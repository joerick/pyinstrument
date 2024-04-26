<script lang="ts">
  import FrameView from './Frame.svelte'
  import type Frame from './model/Frame';
  import type Session from './model/Session';
  import {aggregate_repeated_calls, group_library_frames_processor, merge_consecutive_self_time, remove_first_pyinstrument_frames_processor, remove_importlib, remove_irrelevant_nodes, remove_tracebackhide, remove_unnecessary_self_time_nodes, type ProcessorFunction, type ProcessorOptions} from './model/processors'
  export let session: Session

  const allProcessorsList = [
    remove_importlib,
    remove_tracebackhide,
    merge_consecutive_self_time,
    aggregate_repeated_calls,
    remove_unnecessary_self_time_nodes,
    remove_irrelevant_nodes,
    remove_first_pyinstrument_frames_processor,
    group_library_frames_processor,
  ] as ProcessorFunction[]

  let activeProcessors = allProcessorsList.slice()

  function applyProcessors(rootFrame: Frame, processors: ProcessorFunction[], options: ProcessorOptions) {
    let frame: Frame|null = rootFrame
    for (const processor of processors) {
      frame = processor(frame, options)
      if (!frame) {
        return null
      }
    }
    return frame
  }

  const rootFrame = applyProcessors(session.rootFrame.cloneDeep(), activeProcessors, {session})
</script>

<div class="tree-view">
  {#if !rootFrame}
    <div class="error">
      All frames were filtered out.
    </div>
  {:else}
    <FrameView frame={rootFrame} rootFrame={rootFrame} />
  {/if}
</div>

<style lang="scss">
</style>
