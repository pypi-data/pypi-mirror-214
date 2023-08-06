# Copyright Open Logistics Foundation
#
# Licensed under the Open Logistics Foundation License 1.3.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: OLFL-1.3

"""
Definition of Enums that are used across the mlcvzoo_mmocr package
"""

from mlcvzoo_base.configuration.structs import BaseType


class ClassTypes(BaseType):
    TEXT_CLASS_NAME: str = "text"
    TEXT_CLASS_ID: int = -1
