
# Internal representation

Frames are recorded by the Profiler in a time-linear fashion. While profiling,
the profiler builds a list of frame stacks, with the frames having in format:

    function_name <null> filename <null> function_line_number

When profiling is complete, this list is turned into a tree structure of
Frame objects. This tree contains all the information as gathered by the
profiler, suitable for a flame render.

# Frame objects, the call tree, and processors

The frames are assembled to a call tree by the profiler session. The
time-linearity is retained at this stage.

Before rendering, the call tree is then fed through a sequence of 'processors'
to transform the tree for output.

The most interesting is `aggregate_repeated_calls`, which combines different
instances of function calls into the same frame. This is intuitive as a
summary of where time was spent during execution.

The rest of the processors focus on removing or hiding irrelevant Frames
from the output.

## Self time frames vs. frame.self_time

Self time nodes exist to record time spent in a node, but not in its children.
But normal frame objects can have self_time too. Why? frame.self_time is used
to store the self_time of any nodes that were removed during processing. 
