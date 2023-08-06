from typing import Union

from jsonpath_ng.ext import parse

from gcscore.mod import TargetFieldQuery
from .nodes import NodeRunInOrder, NodeRunInParallel, HasChildren, ComposableNode

__all__ = ['create_target_list', 'flatten']

INSTANCES_JSON_PATH = parse('$.Reservations[*].Instances[*]')


def create_target_list(raw_api_result: list[dict], queries: list[TargetFieldQuery]) -> list[dict]:
    """
    Create an AWS target list from the given API result
    :param raw_api_result:
    :param queries:
    :return: the target list
    """
    raw_instances = list(map(lambda m: m.value, INSTANCES_JSON_PATH.find(raw_api_result)))

    targets = []
    for raw_instance in raw_instances:
        targets.append({q.key: q.find(raw_instance) for q in queries})

    return targets


def flatten(node: HasChildren):
    final_children = []

    node_type = NodeRunInOrder
    if isinstance(node, NodeRunInParallel):
        node_type = NodeRunInParallel
    _ = node_type.__name__

    needs_second_pass = False

    for child in node.gcscore_children:
        # Childless nodes are added as is
        if not isinstance(child, HasChildren):
            final_children.append(child)
            continue

        flatten(child)

        if isinstance(child, node_type):
            # Same node type, all children can be kidnapped
            final_children.extend(child.gcscore_children)
        elif len(child.gcscore_children) == 1:
            # Different node type
            # It can only be taken if there is only one great-child
            final_children.extend(child.gcscore_children)
            needs_second_pass = True
        else:
            # Regular situation, the children cannot be taken
            final_children.append(child)

    node.gcscore_children = final_children
    if needs_second_pass:
        flatten(node)
