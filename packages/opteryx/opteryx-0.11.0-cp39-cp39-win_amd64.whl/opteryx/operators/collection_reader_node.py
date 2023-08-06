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
Collection Reader Node

This is a SQL Query Execution Plan Node.

This Node primarily is used for reading NoSQL sources like MongoDB and Firestore.
"""
import time
from typing import Iterable

import pyarrow

from opteryx.connectors.capabilities import PredicatePushable
from opteryx.models import QueryProperties
from opteryx.models.columns import Columns
from opteryx.operators import BasePlanNode


class CollectionReaderNode(BasePlanNode):
    def __init__(self, properties: QueryProperties, **config):
        """
        The Collection Reader Node is responsible for reading the relevant documents
        from a NoSQL document store and returning a Table/Relation.
        """
        super().__init__(properties=properties)

        self._alias = config.get("alias")
        self._dataset = config["dataset"]
        self._reader = config.get("reader")

        # pushed down selection/filter
        self._selection = config.get("selection")

        self._disable_selections = "NO_PUSH_SELECTION" in config.get("hints", [])

    @property
    def config(self):  # pragma: no cover
        if self._alias:
            return f"{self._dataset} => {self._alias}"
        return f"{self._dataset}"

    @property
    def name(self):  # pragma: no cover
        return "Collection Reader"

    @property
    def can_push_selection(self):
        return isinstance(self._reader, PredicatePushable) and not self._disable_selections

    def push_predicate(self, predicate):
        if self.can_push_selection:
            return self._reader.push_predicate(predicate)
        return False

    def execute(self) -> Iterable:
        metadata = None

        row_count = self._reader.get_document_count(self._dataset)

        for morsel in self._reader.read_documents(self._dataset):
            start_read = time.time_ns()
            self.statistics.time_data_read += time.time_ns() - start_read
            self.statistics.rows_read += morsel.num_rows
            self.statistics.bytes_processed_data += morsel.nbytes
            self.statistics.document_chunks += 1

            if metadata is None:
                morsel = Columns.create_table_metadata(
                    table=morsel,
                    expected_rows=row_count,
                    name=self._dataset,
                    table_aliases=[self._alias],
                    disposition="collection",
                    path=self._dataset,
                )
                metadata = Columns(morsel)
                self.statistics.collections_read += 1
            else:
                morsel = metadata.apply(morsel)

            yield morsel
