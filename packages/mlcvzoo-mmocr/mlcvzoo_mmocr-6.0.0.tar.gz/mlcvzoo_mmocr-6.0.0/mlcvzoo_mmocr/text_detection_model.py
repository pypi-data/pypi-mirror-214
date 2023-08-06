# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Module for defining the model classes that are used to wrap the mmocr framework.
"""

import logging
from typing import Dict, List, Optional, Tuple, Union

from mlcvzoo_base.api.data.annotation_class_mapper import AnnotationClassMapper
from mlcvzoo_base.api.data.class_identifier import ClassIdentifier
from mlcvzoo_base.api.data.segmentation import Segmentation
from mlcvzoo_base.api.model import SegmentationModel
from mlcvzoo_mmdetection.model import MMDetectionModel
from mmocr.apis.inferencers import TextDetInferencer
from mmocr.structures.textdet_data_sample import TextDetDataSample
from nptyping import Int, NDArray, Shape

from mlcvzoo_mmocr.configuration import MMOCRConfig
from mlcvzoo_mmocr.model import MMOCRModel

logger = logging.getLogger(__name__)

ImageType = NDArray[Shape["Height, Width, Any"], Int]


class MMOCRTextDetectionModel(
    MMOCRModel[Segmentation],
    SegmentationModel[MMOCRConfig, Union[str, ImageType]],
):
    def __init__(
        self,
        from_yaml: Optional[str] = None,
        configuration: Optional[MMOCRConfig] = None,
        string_replacement_map: Optional[Dict[str, str]] = None,
        init_for_inference: bool = False,
        is_multi_gpu_instance: bool = False,
    ) -> None:
        self.inferencer: Optional[TextDetInferencer] = None

        MMOCRModel.__init__(
            self,
            from_yaml=from_yaml,
            configuration=configuration,
            string_replacement_map=string_replacement_map,
            init_for_inference=init_for_inference,
            is_multi_gpu_instance=is_multi_gpu_instance,
        )
        SegmentationModel.__init__(
            self,
            configuration=self.configuration,
            init_for_inference=init_for_inference,
            mapper=AnnotationClassMapper(
                class_mapping=self.configuration.class_mapping,
            ),
        )

    def _init_inference_model(self) -> None:
        if self.net is None:
            self.inferencer = TextDetInferencer(self.cfg, None)

            self.net = self.inferencer.model

            if self.configuration.inference_config.checkpoint_path != "":
                self.restore(
                    checkpoint_path=self.configuration.inference_config.checkpoint_path
                )

    @property
    def num_classes(self) -> int:
        return self.mapper.num_classes

    def get_classes_id_dict(self) -> Dict[int, str]:
        return self.mapper.annotation_class_id_to_model_class_name_map

    def __decode_mmocr_result(
        self, prediction: TextDetDataSample
    ) -> List[Segmentation]:
        segmentations: List[Segmentation] = []
        for polygons, score in zip(
            prediction.pred_instances.polygons, prediction.pred_instances.scores
        ):
            float_score = float(score)
            if float_score < self.configuration.inference_config.score_threshold:
                continue

            polygon_iterator = iter(polygons)

            segmentations.extend(
                self.build_segmentations(
                    class_identifiers=[
                        ClassIdentifier(
                            class_id=MMOCRConfig.__text_class_id__,
                            class_name=MMOCRConfig.__text_class_name__,
                        )
                    ],
                    score=score,
                    polygon=list(zip(polygon_iterator, polygon_iterator)),
                )
            )

            # TODO: Move directly into the "build_segmentation" method?
            if self.configuration.inference_config.to_rect_polygon:
                for segmentation in segmentations:
                    segmentation.to_rect_polygon()

        return segmentations

    def predict(
        self, data_item: Union[str, ImageType]
    ) -> Tuple[Union[str, ImageType], List[Segmentation]]:
        if self.net is None:
            raise ValueError(
                "The 'net' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )
        if self.inferencer is None:
            raise ValueError(
                "The 'inferencer' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )

        # For a single data_item we only have one prediction
        return data_item, self.__decode_mmocr_result(
            self.inferencer(
                data_item, return_datasamples=True, batch_size=1, progress_bar=False
            )["predictions"][0]
        )

    def predict_many(
        self, data_items: List[Union[str, ImageType]]
    ) -> List[Tuple[Union[str, ImageType], List[Segmentation]]]:
        if self.net is None:
            raise ValueError(
                "The 'net' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )
        if self.inferencer is None:
            raise ValueError(
                "The 'inferencer' attribute is not initialized, "
                "make sure to instantiate with init_for_inference=True"
            )

        prediction_list: List[Tuple[Union[str, ImageType], List[Segmentation]]] = []

        # TODO: add batch-size as parameter
        predictions: List[TextDetDataSample] = self.inferencer(
            data_items,
            return_datasamples=True,
            batch_size=len(data_items),
            progress_bar=False,
        )["predictions"]

        for data_item, prediction in zip(data_items, predictions):
            segmentations = self.__decode_mmocr_result(prediction=prediction)

            prediction_list.append(
                (
                    data_item,
                    segmentations,
                )
            )

        return prediction_list


if __name__ == "__main__":
    MMDetectionModel.run(MMOCRTextDetectionModel)
