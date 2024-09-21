<script lang="ts">
  import FrameView from './Frame.svelte'
  import type Frame from '../lib/model/Frame';
  import type Session from '../lib/model/Session';
  import { applyProcessors } from '../lib/model/modelUtil';
  import {aggregate_repeated_calls, group_library_frames_processor, merge_consecutive_self_time, remove_first_pyinstrument_frames_processor, remove_importlib, remove_irrelevant_nodes, remove_tracebackhide, remove_unnecessary_self_time_nodes, type ProcessorFunction, type ProcessorOptions, allProcessors, type Processor} from '../lib/model/processors'
  export let session: Session
  import { viewOptionsCallStack } from '../lib/settings';
  import { derived } from 'svelte/store';

  const config = derived([viewOptionsCallStack], ([viewOptionsCallStack]) => {
    const processors = [
      viewOptionsCallStack.removeImportlib ? remove_importlib : null,
      viewOptionsCallStack.removeTracebackHide ? remove_tracebackhide : null,
      merge_consecutive_self_time,
      aggregate_repeated_calls,
      remove_unnecessary_self_time_nodes,
      viewOptionsCallStack.removeIrrelevant ? remove_irrelevant_nodes : null,
      viewOptionsCallStack.removePyinstrument ? remove_first_pyinstrument_frames_processor : null,
      viewOptionsCallStack.collapseMode !== 'disabled' ? group_library_frames_processor : null,
    ].filter(p => p !== null)
    const options = {
      filterThreshold: viewOptionsCallStack.removeIrrelevantThreshold,
      hideRegex: viewOptionsCallStack.collapseMode == 'custom' ? viewOptionsCallStack.collapseCustomHide : undefined,
      showRegex: viewOptionsCallStack.collapseMode == 'custom' ? viewOptionsCallStack.collapseCustomShow : undefined,
    } as ProcessorOptions
    return {processors, options}
  })

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), $config.processors, $config.options)
</script>

<div class="tree-view">
  <div class="spacer" style="height: 20px;"></div>
  <div class="margins">
    {#if !rootFrame}
      <div class="error">
        All frames were filtered out.
      </div>
    {:else}
      <FrameView frame={rootFrame} rootFrame={rootFrame} />
    {/if}
  </div>
</div>

<style lang="scss">
</style>
