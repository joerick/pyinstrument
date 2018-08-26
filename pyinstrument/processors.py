from operator import methodcaller

'''
Processors are functions that take a Frame object, and mutate the tree to perform some task.

They can mutate the tree in-place, but also can change the root frame, they should always be
called like:

    frame = processor(frame)
'''

def remove_importlib(frame):
    # iterate over a copy of the children since it's going to mutate while we're iterating
    for child in frame.children:
        remove_importlib(child)

        if '<frozen importlib._bootstrap' in child.file_path:
            # remove this node, moving the self_time and children up to the parent
            frame.self_time += child.self_time
            frame.add_children(child.children, after=child)
            child.remove_from_parent()

    return frame


def aggregate_repeated_calls(frame):
    '''
    Converts a timeline into a time-aggregate summary.

    Adds together calls along the same call stack, so that repeated calls appear as the same
    frame. Removes time-linearity - frames are sorted according to total time spent.

    Useful for outputs that display a summary of execution (e.g. text and html outputs)
    '''
    children_by_identifier = {}

    # iterate over a copy of the children since it's going to mutate while we're iterating
    for child in frame.children:
        if child.identifier in children_by_identifier:
            aggregate_frame = children_by_identifier[child.identifier]

            # combine the two frames, putting the children and self_time into the aggregate frame.
            aggregate_frame.self_time += child.self_time
            aggregate_frame.add_children(child.children)

            # remove this frame, it's been incorporated into aggregate_frame
            child.remove_from_parent()
        else:
            # never seen this identifier before. It becomes the aggregate frame.
            children_by_identifier[child.identifier] = child

    # recurse into the children
    for child in frame.children:
        aggregate_repeated_calls(child)

    # sort the children by time
    # it's okay to use the internal _children list, sinde we're not changing the tree
    # structure.
    frame._children.sort(key=methodcaller('time'), reverse=True)  # pylint: disable=W0212

    return frame

def default_time_aggregate_processors():
    return [
        remove_importlib,
        aggregate_repeated_calls
    ]

def default_timeline_processors():
    return [
        remove_importlib,
    ]
