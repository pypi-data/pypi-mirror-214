# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Calendar month operator class and public API function definitions."""

from temporian.core import operator_lib
from temporian.core.data.node import Node
from temporian.core.operators.calendar.base import BaseCalendarOperator


class CalendarMonthOperator(BaseCalendarOperator):
    """
    Calendar operator to obtain the month each timestamp belongs to.
    """

    @classmethod
    def operator_def_key(cls) -> str:
        return "CALENDAR_MONTH"

    @classmethod
    def output_feature_name(cls) -> str:
        return "calendar_month"


operator_lib.register_operator(CalendarMonthOperator)


def calendar_month(sampling: Node) -> Node:
    """Obtains the month the timestamps in a node's sampling are in.

    Features in the input node are ignored, only the timestamps in
    `Node.sampling` are used and they must be unix timestamps
    (check  `Node.sampling.is_unix_timestamp`).

    Output feature contains numbers between
    1 and 12.

    Args:
        sampling: Node with unix timestamp sampling.

    Returns:
        Single feature with the month each timestamp in `sampling` belongs to.
    """
    return CalendarMonthOperator(sampling).outputs["output"]
