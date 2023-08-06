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
This module contains support functions for working with PyArrow
"""

import pyarrow
from orjson import dumps
from orjson import loads

INTERNAL_BATCH_SIZE = 500


def limit_records(morsels, limit):
    """
    Cycle over an iterable of morsels, limiting the response to a given
    number of records.
    """
    row_count = 0
    result_set = []
    morsels_iterator = iter(morsels)

    morsel = None
    while row_count < limit:
        try:
            morsel = next(morsels_iterator)
        except StopIteration:
            break

        if morsel.num_rows > 0:
            if row_count + morsel.num_rows <= limit:
                # append whole morsel to result_set
                result_set.append(morsel)
                row_count += morsel.num_rows
            else:
                # slice morsel to only append needed rows to result_set
                num_rows_needed = limit - row_count
                result_set.append(morsel.slice(offset=0, length=num_rows_needed))
                row_count = limit

    if len(result_set) == 0:
        if morsel is None:
            morsel = next(morsels_iterator, None)
        if morsel is None:
            return None
        return pyarrow.Table.from_batches([], schema=morsel.schema)
    else:
        return pyarrow.concat_tables(result_set, promote=True)


def rename_columns(morsels):
    """rename columns to their preferred names"""
    from opteryx.models import Columns

    columns = None
    morsels = iter(morsels)
    for morsel in morsels:
        if morsel is None:
            break
        if columns is None and morsel is not None:
            columns = Columns(morsel)
            preferred_names = columns.preferred_column_names
            column_names = []
            for col in morsel.column_names:
                column_names.append([c for a, c in preferred_names if a == col][0])
        if column_names and morsel is not None:
            yield morsel.rename_columns(column_names)


# Adapted from:
# https://stackoverflow.com/questions/55546027/how-to-assign-arbitrary-metadata-to-pyarrow-table-parquet-columns


def set_metadata(table, table_metadata=None, column_metadata=None):
    """
    Store table-level metadata as json-encoded byte strings.

    Table-level metadata is stored in the table's schema.

    parameters:
        table: pyarrow.Table
            The table to store metadata in
        col_meta: dict
            A json-serializable dictionary with column metadata in the form
            {
                'column_1': {'some': 'data', 'value': 1},
                'column_2': {'more': 'stuff', 'values': [1,2,3]}
            }
        tbl_meta: dict
            A json-serializable dictionary with table-level metadata.
    """

    # Create updated column fields with new metadata
    if table_metadata or column_metadata:
        fields = []
        for name in table.schema.names:
            col = table.field(name)
            if col.name in column_metadata:
                # Get updated column metadata
                metadata = col.metadata or {}
                for k, v in column_metadata[name].items():
                    if isinstance(k, str):
                        k = k.encode()
                    metadata[k] = dumps(v)
                # Update field with updated metadata
                fields.append(col.with_metadata(metadata))
            else:
                fields.append(col)

        # Get updated table metadata
        tbl_metadata = table.schema.metadata or {}
        if table_metadata:
            for k, v in table_metadata.items():
                if isinstance(v, bytes):
                    tbl_metadata[k] = v
                else:
                    tbl_metadata[k] = dumps(v)

        # Create new schema with updated table metadata
        schema = pyarrow.schema(fields, metadata=tbl_metadata)
        # With updated schema build new table (shouldn't copy data)
        table = table.cast(schema)

    return table


def _decode_metadata(metadata):
    """
    Arrow stores metadata keys and values as bytes. We store "arbitrary" data as
    json-encoded strings (utf-8), which are here decoded into normal dict.
    """

    if not metadata:
        # None or {} are not decoded
        return {}

    decoded = {}
    for key, value in metadata.items():
        key = key.decode("utf-8")
        val = loads(value)
        decoded[key] = val
    return decoded


def table_metadata(tbl):
    """Get table metadata as dict."""
    return _decode_metadata(tbl.schema.metadata)


def column_metadata(tbl):
    """Get column metadata as dict."""
    return {col: _decode_metadata(tbl.field(col).metadata) for col in tbl.schema.names}


def coerce_columns(table, column_names):
    """convert numeric types to a common type to allow comparisons"""
    # get the column we're coercing
    my_schema = table.schema

    if not isinstance(column_names, list):
        column_names = [column_names]

    for column_name in column_names:
        index = table.column_names.index(column_name)
        column = my_schema.field(column_name)

        # if it's numeric, and not already the type we want, convert it
        if str(column.type) in ("int64", "double"):
            column = column.with_type(pyarrow.float64())
            my_schema = my_schema.set(index, pyarrow.field(column_name, pyarrow.float64()))
            table = table.cast(target_schema=my_schema)

    return table
