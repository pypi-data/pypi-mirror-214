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
import orjson

from opteryx import operators
from opteryx.components.logical_planner import builders
from opteryx.components.logical_planner import custom_builders
from opteryx.connectors import DiskConnector
from opteryx.connectors import connector_factory
from opteryx.exceptions import DatabaseError
from opteryx.exceptions import ProgrammingError
from opteryx.exceptions import SqlError
from opteryx.managers.expression import NodeType
from opteryx.managers.expression import deduplicate_list_of_nodes
from opteryx.managers.expression import get_all_nodes_of_type
from opteryx.models import ExecutionTree
from opteryx.models.node import Node
from opteryx.utils import paths


def explain_query(ast, properties):
    # we're handling two plans here:
    # - plan - this is the plan for the query we're exlaining
    # - my_plan - this is the plan for this query

    from opteryx.components.query_planner import QueryPlanner

    query_planner = QueryPlanner(properties=properties)
    plan = query_planner.create_logical_plan(ast["Explain"]["statement"])
    plan = query_planner.optimize_plan(plan)
    my_plan = ExecutionTree()
    explain_node = operators.ExplainNode(properties, query_plan=plan)
    my_plan.add_node("explain", explain_node)
    return my_plan


def select_query(ast, properties):
    """
    The planner creates the naive query plan.

    The goal here is to create a plan that's only guarantee is the response is correct.
    It doesn't try to make it performant, low-memory or any other measure of 'good'
    beyond correctness.
    """
    plan = ExecutionTree()

    properties.ctes = custom_builders.extract_ctes(ast["Query"], properties.qid)

    all_identifiers = (
        set(custom_builders.extract_identifiers(ast)) - custom_builders.WELL_KNOWN_HINTS
    )
    try:
        _relations = list(
            custom_builders.extract_relations(
                ast["Query"]["body"]["Select"]["from"], properties.qid
            )
        )
    except IndexError:
        _relations = []

    # if we have no relations, use the $no_table relation
    if len(_relations) == 0:
        _relations = [
            custom_builders.RelationDescription(
                dataset="$no_table", kind="Internal", cache=properties.cache
            )
        ]

    # We always have a data source - even if it's 'no table'
    relation = _relations[0]

    reader = None
    if isinstance(relation.dataset, str) and relation.dataset in properties.ctes:
        # CTEs look like subqueries
        relation.kind = "SubQuery"
        relation.alias = relation.dataset
        relation.dataset = properties.ctes[relation.dataset]
    if relation.kind == "File":
        reader = DiskConnector(prefix="")
    elif relation.kind == "External":
        # external comes in different flavours
        reader = connector_factory(relation.dataset)
        relation.kind = reader.__mode__

    plan.add_node(
        "from",
        operators.reader_factory(relation.kind)(
            properties=properties,
            alias=relation.alias,
            dataset=relation.dataset,
            reader=reader,
            cache=relation.cache,
            start_date=relation.start_date,
            end_date=relation.end_date,
            hints=relation.hints,
            selection=all_identifiers,
        ),
    )
    last_node = "from"

    _joins = list(custom_builders.extract_joins(ast, properties.qid))
    if len(_joins) == 0 and len(_relations) == 2:
        # If there's no explicit JOIN but the query has two relations, we
        # use a CROSS JOIN
        _joins = [("CrossJoin", _relations[1], None, None)]
    for join_id, _join in enumerate(_joins):
        if _join:
            join_type, right, join_on, join_using = _join
            if join_type == "CrossJoin" and right.kind == "Function":
                join_type = "CrossJoinUnnest"
            else:
                dataset = right.dataset
                if isinstance(dataset, ExecutionTree):
                    mode = "Blob"  # subqueries are here due to legacy reasons
                    reader = None
                elif isinstance(dataset, dict) and dataset.get("function") is not None:
                    mode = "Function"
                    reader = None
                elif dataset[0:1] == "$":
                    mode = "Internal"
                    reader = None
                elif dataset in properties.ctes:
                    # CTEs look like subqueries
                    mode = "SubQuery"  # subqueries are here due to legacy reasons
                    reader = None
                    right.alias = right.dataset
                    right.dataset = properties.ctes[dataset]
                elif paths.is_file(dataset):
                    mode = "File"
                else:
                    reader = connector_factory(dataset)
                    mode = reader.__mode__

                # Otherwise, the right table needs to come from the Reader
                right = operators.reader_factory(mode)(
                    properties=properties,
                    dataset=right.dataset,
                    alias=right.alias,
                    reader=reader,
                    cache=relation.cache,
                    start_date=right.start_date,
                    end_date=right.end_date,
                    hints=right.hints,
                )

            join_node = operators.join_factory(join_type)
            if join_node is None:
                raise SqlError(f"Join type not supported - `{_join[0]}`")

            plan.add_node(
                f"join-{join_id}",
                join_node(
                    properties=properties,
                    join_type=join_type,
                    join_on=join_on,
                    join_using=join_using,
                ),
            )
            plan.add_edge(last_node, f"join-{join_id}")

            plan.add_node(f"join-{join_id}-right", right)
            plan.add_edge(f"join-{join_id}-right", f"join-{join_id}", "right")

            last_node = f"join-{join_id}"

    _selection = builders.build(ast["Query"]["body"]["Select"]["selection"])
    if _selection:
        plan.add_node(
            "where",
            operators.SelectionNode(properties, filter=_selection),
        )
        plan.add_edge(last_node, "where")
        last_node = "where"

    _projection = builders.build(ast["Query"]["body"]["Select"]["projection"])
    _groups = builders.build(ast["Query"]["body"]["Select"]["group_by"])
    if _groups or get_all_nodes_of_type(
        _projection, select_nodes=(NodeType.AGGREGATOR, NodeType.COMPLEX_AGGREGATOR)
    ):
        _aggregates = _projection.copy()
        if isinstance(_aggregates, dict):
            raise SqlError("GROUP BY cannot be used with SELECT *")
        plan.add_node(
            "agg",
            operators.AggregateNode(properties, aggregates=_aggregates, groups=_groups),
        )
        plan.add_edge(last_node, "agg")
        last_node = "agg"

    _having = builders.build(ast["Query"]["body"]["Select"]["having"])
    if _having:
        plan.add_node(
            "having",
            operators.SelectionNode(properties, filter=_having),
        )
        plan.add_edge(last_node, "having")
        last_node = "having"

    # collect ORDER BY now, so we can keep any columns in the ORDER BY clause too
    _order = custom_builders.extract_order(ast)
    reproject = None

    if _order and (_projection[0].node_type != NodeType.WILDCARD):
        order_fields = [f[0][0] for f in _order if f[0][0].node_type == NodeType.IDENTIFIER]
        reproject = _projection.copy()
        _projection.extend(order_fields)
        # aliases appear in the list as different fields here, so dedupe and see if the
        # lists are different lengths
        _projection = deduplicate_list_of_nodes(_projection)
        if len(_projection) == len(reproject):
            reproject = None

    # qualified wildcards have the qualifer in the value
    # e.g. SELECT table.* -> node.value = table
    if (_projection[0].node_type != NodeType.WILDCARD) or (_projection[0].value is not None):
        plan.add_node(
            "select",
            operators.ProjectionNode(properties, projection=_projection),
        )
        plan.add_edge(last_node, "select")
        last_node = "select"

    _distinct = custom_builders.extract_distinct(ast)
    if _distinct:
        plan.add_node("distinct", operators.DistinctNode(properties))
        plan.add_edge(last_node, "distinct")
        last_node = "distinct"

    if _order:
        plan.add_node("order", operators.SortNode(properties, order=_order))
        plan.add_edge(last_node, "order")
        last_node = "order"

    # if we need to project after the order by
    if reproject:
        plan.add_node(
            "post_order_select",
            operators.ProjectionNode(properties, projection=reproject),
        )
        plan.add_edge(last_node, "post_order_select")
        last_node = "post_order_select"

    _offset = custom_builders.extract_offset(ast)
    if _offset:
        plan.add_node(
            "offset",
            operators.OffsetNode(properties, offset=_offset),
        )
        plan.add_edge(last_node, "offset")
        last_node = "offset"

    _limit = custom_builders.extract_limit(ast)
    # 0 limit is valid
    if _limit is not None:
        plan.add_node("limit", operators.LimitNode(properties, limit=_limit))
        plan.add_edge(last_node, "limit")
        last_node = "limit"

    _insert = custom_builders.extract_into(ast)

    return plan


def set_variable_query(ast, properties):
    """put variables defined in SET statements into context"""
    key = ast["SetVariable"]["variable"][0]["value"]
    value = builders.build(ast["SetVariable"]["value"][0]["Value"])
    if key[0] == "@":  # pragma: no cover
        properties.variables[key] = value
    else:
        key = key.lower()
        if key in properties.read_only_properties:
            raise ProgrammingError(f"Invalid parameter '{key}'")
        if hasattr(properties, key):
            setattr(properties, key, value.value)
        else:
            raise ProgrammingError(
                f"Unknown parameter, variables must be prefixed with a '@' - '{key}'"
            )

    # return a plan, because it's expected
    plan = ExecutionTree()
    operator = operators.ShowValueNode(key="result", value="Complete", properties=properties)
    plan.add_node("show", operator)
    return plan


def show_columns_query(ast, properties):
    plan = ExecutionTree()
    dataset = ".".join([part["value"] for part in ast["ShowColumns"]["table_name"]])

    if dataset[0:1] == "$":
        mode = "Internal"
        reader = None
    else:
        reader = connector_factory(dataset)
        mode = reader.__mode__

    plan.add_node(
        "reader",
        operators.reader_factory(mode)(
            properties=properties,
            dataset=dataset,
            alias=None,
            reader=reader,
            cache=None,  # never read from cache
            start_date=ast["ShowColumns"]["table_name"][0]["start_date"],
            end_date=ast["ShowColumns"]["table_name"][0]["end_date"],
        ),
    )
    last_node = "reader"

    filters = custom_builders.extract_show_filter(ast["ShowColumns"])
    if filters:
        plan.add_node(
            "filter",
            operators.ColumnFilterNode(properties=properties, filter=filters),
        )
        plan.add_edge(last_node, "filter")
        last_node = "filter"

    plan.add_node(
        "columns",
        operators.ShowColumnsNode(
            properties=properties,
            full=ast["ShowColumns"]["full"],
            extended=ast["ShowColumns"]["extended"],
        ),
    )
    plan.add_edge(last_node, "columns")
    last_node = "columns"

    return plan


def show_create_query(ast, properties):
    plan = ExecutionTree()

    if ast["ShowCreate"]["obj_type"] != "Table":
        raise SqlError("SHOW CREATE only supports tables")

    dataset = ".".join([part["value"] for part in ast["ShowCreate"]["obj_name"]])

    if dataset[0:1] == "$":
        mode = "Internal"
        reader = None
    else:
        reader = connector_factory(dataset)
        mode = reader.__mode__

    plan.add_node(
        "reader",
        operators.reader_factory(mode)(
            properties=properties,
            dataset=dataset,
            alias=None,
            reader=reader,
            cache=None,  # never read from cache
            start_date=ast["ShowCreate"]["start_date"],
            end_date=ast["ShowCreate"]["end_date"],
        ),
    )
    last_node = "reader"

    plan.add_node(
        "show_create",
        operators.ShowCreateNode(properties=properties, table=dataset),
    )
    plan.add_edge(last_node, "show_create")
    last_node = "show_create"

    return plan


def show_variable_query(ast, properties):
    """
    This is the generic SHOW <variable> handler - there are specific handlers
    for some keywords after SHOW, like SHOW COLUMNS.

    SHOW <variable> only really has a single node.

    All of the keywords should up as a 'values' list in the variable in the ast.
    """

    plan = ExecutionTree()
    name_column = None

    keywords = [value["value"].upper() for value in ast["ShowVariable"]["variable"]]
    if keywords[0] == "PARAMETER":
        if len(keywords) != 2:
            raise SqlError("`SHOW PARAMETER` expects a single parameter name.")
        key = keywords[1].lower()
        if not hasattr(properties, key) or key == "variables":
            raise SqlError(f"Unknown parameter '{key}'.")
        value = getattr(properties, key)

        show_node = "show_parameter"
        node = operators.ShowValueNode(properties=properties, key=key, value=value)
        plan.add_node(show_node, node)
    elif keywords[0] == "DATABASES":
        if len(keywords) != 1:
            raise SqlError(f"`SHOW DATABASES` end expected, got '{keywords[1]}'")
        show_node = "show_databases"
        node = operators.ShowDatabasesNode(properties=properties)  # type:ignore
        plan.add_node(show_node, node)
        name_column = Node(NodeType.IDENTIFIER, value="Database")
    else:  # pragma: no cover
        raise SqlError(f"SHOW statement type not supported for `{keywords[0]}`.")

    if name_column is None:
        name_column = Node(NodeType.IDENTIFIER, value="name")

    order_by_node = operators.SortNode(
        properties=properties,
        order=[([name_column], "ascending")],
    )
    plan.add_node("order", order_by_node)
    plan.add_edge(show_node, "order")

    return plan


def show_functions_query(ast, properties):
    """show the supported functions, optionally filter them"""
    plan = ExecutionTree()

    show = operators.ShowFunctionsNode(properties=properties)
    plan.add_node("show", show)
    last_node = "show"

    filters = custom_builders.extract_show_filter(ast["ShowFunctions"])
    if filters:
        plan.add_node(
            "filter",
            operators.SelectionNode(properties=properties, filter=filters),
        )
        plan.add_edge(last_node, "filter")

    return plan


def show_variables_query(ast, properties):
    """show the known variables, optionally filter them"""
    plan = ExecutionTree()

    show = operators.ShowVariablesNode(properties=properties)
    plan.add_node("show", show)
    last_node = "show"

    filters = custom_builders.extract_show_filter(ast["ShowVariables"], "variable_name")
    if filters:
        plan.add_node(
            "filter",
            operators.SelectionNode(properties=properties, filter=filters),
        )
        plan.add_edge(last_node, "filter")

    return plan


def analyze_query(ast, properties):
    """build statistics for a table"""

    # TODO: [TARCHIA] - get a list of all of the blobs for this dataset and trigger add
    # requests to Tarchia - this will add/update the statistics for the blob

    plan = ExecutionTree()
    dataset = ".".join([part["value"] for part in ast["Analyze"]["table_name"]])

    if dataset[0:1] == "$":
        mode = "Internal"
        reader = None
    else:
        if paths.is_file(dataset):
            mode = "File"
            reader = DiskConnector(prefix="")
        else:
            reader = connector_factory(dataset)
            mode = reader.__mode__

    plan.add_node(
        "reader",
        operators.reader_factory(mode)(
            properties=properties,
            dataset=dataset,
            alias=None,
            reader=reader,
            cache=None,  # never read from cache
            start_date=ast["Analyze"]["table_name"][0]["start_date"],
            end_date=ast["Analyze"]["table_name"][0]["end_date"],
        ),
    )
    last_node = "reader"

    plan.add_node(
        "buildstats",
        operators.BuildStatisticsNode(properties=properties),
    )
    plan.add_edge(last_node, "buildstats")

    return plan


def execute_query(ast, properties):
    """execute a prepared statement"""
    try:
        statement_name = ast["Execute"]["name"]["value"]
        parameters = [builders.build(p["Value"]) for p in ast["Execute"]["parameters"]]
        prepared_statatements = orjson.loads(open("prepared_statements.json").read())
        if statement_name not in prepared_statatements:
            raise SqlError("Unable to EXECUTE prepared statement, '{statement_name}' not defined.")
        prepared_statement = prepared_statatements[statement_name]

        from opteryx.components.query_planner import QueryPlanner
        from opteryx.components.sql_rewriter.sql_rewriter import clean_statement
        from opteryx.components.sql_rewriter.sql_rewriter import remove_comments
        from opteryx.components.sql_rewriter.temporal_extraction import extract_temporal_filters

        # these would have been applied to the EXECUTE statement, we want to do them on the
        # prepared statement
        statement = remove_comments(prepared_statement)
        statement = clean_statement(statement)
        statement, properties.temporal_filters = extract_temporal_filters(statement)

        # we need to plan the prepared statement
        query_planner = QueryPlanner(properties=properties, statement=statement)
        asts = list(query_planner.parse_and_lex())
        if len(asts) != 1:
            raise SqlError("Cannot execute prepared batch statements.")
        query_planner.test_paramcount(asts, parameters)
        prepared_ast = query_planner.bind_ast(asts[0], parameters=parameters)
        plan = query_planner.create_logical_plan(prepared_ast)
        # optimize is the next step, so don't need to do it here
        return plan

    except OSError as err:
        raise DatabaseError(
            "Unable to EXECUTE prepared statement, cannot find definitions."
        ) from err


def use_query(ast, properties):
    # TODO - set the default database in the connection
    plan = ExecutionTree()
    plan.add_node(
        "no_op_one",
        operators.NoOpNode(properties=properties),
    )
    plan.add_node(
        "no_op_two",
        operators.NoOpNode(properties=properties),
    )
    # two noop nodes to make a graph
    plan.add_edge("no_op_one", "no_op_two")
    return plan


# wrappers for the query builders
QUERY_BUILDER = {
    "Analyze": analyze_query,
    "Execute": execute_query,
    "Explain": explain_query,
    "Query": select_query,
    "SetVariable": set_variable_query,
    "ShowColumns": show_columns_query,
    "ShowCreate": show_create_query,
    "ShowFunctions": show_functions_query,
    "ShowVariable": show_variable_query,  # generic SHOW handler
    "ShowVariables": show_variables_query,
    "Use": use_query,
}
