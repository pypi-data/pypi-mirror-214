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
This is a temporary step, which takes logical plans from the V2 planner
and converts them to V1 physical plans.
"""

from opteryx import operators
from opteryx.components.v2.logical_planner import LogicalPlanStepType
from opteryx.models import ExecutionTree
from opteryx.models import QueryProperties


def create_physical_plan(logical_plan):
    plan = ExecutionTree()

    query_properties = QueryProperties(qid=0)

    for nid, logical_node in logical_plan.nodes(data=True):
        node_type = logical_node.node_type
        node_config = logical_node.properties
        node: operators.BasePlanNode = None

        if node_type == LogicalPlanStepType.Aggregate:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Distinct:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Explain:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Fake:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Filter:
            node = operators.SelectionNode(query_properties, filter=node_config["condition"])
        elif node_type == LogicalPlanStepType.GenerateSeries:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Group:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Join:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Order:
            node = operators.NoOpNode(query_properties, **node_config)
        #           we need a gen 2 order by that doesn't rely on the columns object
        #            node = operators.SortNode(query_properties, order=node_config["order_by"])
        elif node_type == LogicalPlanStepType.Project:
            print(node_config)
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Scan:
            node = operators.V2ScannerNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Show:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.ShowColumns:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Subquery:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Unnest:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Union:
            node = operators.NoOpNode(query_properties, **node_config)
        elif node_type == LogicalPlanStepType.Values:
            node = operators.NoOpNode(query_properties, **node_config)
        else:
            raise Exception(f"something unexpected happed - {node_type.name}")

        plan.add_node(nid, node)

    for source, destination, relation in logical_plan.edges():
        plan.add_edge(source, destination)

    return plan
