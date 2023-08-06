# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Distinct Node

This is a SQL Query Execution Plan Node.

This Node is used to evaluate the filters on SHOW queries e.g.: 

- SHOW COLUMNS
- SHOW VARIABLES

It expects the filter to be applied to the 'name' column.
"""
from typing import Iterable

from opteryx.exceptions import SqlError
from opteryx.models import Columns
from opteryx.models import QueryProperties
from opteryx.operators import BasePlanNode


class ColumnFilterNode(BasePlanNode):
    def __init__(self, properties: QueryProperties, **config):
        super().__init__(properties=properties)
        self._filter = config.get("filter", True)

    @property
    def config(self):  # pragma: no cover
        return ""

    @property
    def greedy(self):  # pragma: no cover
        return True

    @property
    def name(self):  # pragma: no cover
        return "Select Columns"

    def execute(self) -> Iterable:
        if len(self._producers) != 1:  # pragma: no cover
            raise SqlError(f"{self.name} on expects a single producer")

        morsels = self._producers[0]  # type:ignore

        selection = None
        columns = None

        for morsel in morsels.execute():
            if selection is None:
                columns = Columns(morsel)
                selection = list(dict.fromkeys(columns.filter(self._filter)))
            morsel = morsel.select(selection)
            yield columns.apply(morsel)
