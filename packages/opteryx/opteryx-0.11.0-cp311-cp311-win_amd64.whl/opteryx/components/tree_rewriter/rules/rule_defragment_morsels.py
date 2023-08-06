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
Optimization Rule - Defragment morsels

Type: Heuristic
Goal: Reduce small units of work
"""
from opteryx import operators
from opteryx.models.execution_tree import ExecutionTree
from opteryx.utils import random_string


def defragment_morsels(plan: ExecutionTree, properties):
    """
    In a block/chunk iterator model, most of the performance improvement comes from
    fewer handoffs between operators (fewer function calls) and being able to
    use vectorization and SIMD across multiple datasets at the same time.

    This benefit is lessened if the chunks passing through the system are very
    small. This action adds a defragmentation step to the plan to help ensure
    activities which most benefit from full morsels are more likely to get them.

    This presently only works on adjacent morsels - so does not scan the entire
    partition or query set looking for morsels to merge.
    """

    # exit ASAP if disabled
    if not properties.enable_morsel_defragmentation:
        return plan

    # find the in-scope nodes
    selection_nodes = plan.get_nodes_of_type(operators.SelectionNode)

    # killer questions - if any aren't met, bail
    if selection_nodes is None:
        return plan

    # HAVING and WHERE are selection nodes
    for nid in selection_nodes:
        # get the node from the node_id
        defrag = operators.MorselDefragmentNode(properties=properties)
        plan.insert_node_before(f"defrag-{random_string()}", defrag, nid)

    return plan
