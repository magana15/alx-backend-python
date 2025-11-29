from collections import defaultdict

def build_message_tree(messages):
    """
    Given an *iterable* (QuerySet) of Message objects ordered by timestamp,
    return a list of root messages where each message object gets an attribute
    `.children` = list of Message replies (nested).
    This builds the tree in memory in O(n).
    """
    # Ensure messages is a list so we can iterate multiple times
    messages = list(messages)

    children_map = defaultdict(list)
    message_by_id = {}

    for msg in messages:
        message_by_id[msg.pk] = msg
        # initialize children container
        setattr(msg, "children", [])

    # attach each message to its parent's children list (if parent exists)
    for msg in messages:
        if msg.parent_message_id:
            children_map[msg.parent_message_id].append(msg)
        else:
            # root messages are those without a parent
            children_map[None].append(msg)

    # now set children lists (preserving order)
    for parent_id, children in children_map.items():
        if parent_id is None:
            continue
        parent = message_by_id.get(parent_id)
        if parent:
            parent.children = children

    # At last, ensure the root list also has children recursively populated:
    # children_map[None] contains root messages (in timestamp order if original query was ordered)
    root_messages = children_map[None]
    return root_messages
