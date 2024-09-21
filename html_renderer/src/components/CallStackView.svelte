<script lang="ts">
  import FrameView from './Frame.svelte'
  import type Frame from '../lib/model/Frame';
  import type Session from '../lib/model/Session';
  import { applyProcessors } from '../lib/model/modelUtil';
  import {aggregate_repeated_calls, group_library_frames_processor, merge_consecutive_self_time, remove_first_pyinstrument_frames_processor, remove_importlib, remove_irrelevant_nodes, remove_tracebackhide, remove_unnecessary_self_time_nodes, type ProcessorFunction, type ProcessorOptions, allProcessors, type Processor} from '../lib/model/processors'
  export let session: Session
  import { viewOptionsCallStack } from '../lib/settings';
  import { derived } from 'svelte/store';

  // const defaultProcessorFunctions = [
  //   remove_importlib,
  //   remove_tracebackhide,
  //   merge_consecutive_self_time,
  //   aggregate_repeated_calls,
  //   remove_unnecessary_self_time_nodes,
  //   remove_irrelevant_nodes,
  //   remove_first_pyinstrument_frames_processor,
  //   group_library_frames_processor,
  // ] as ProcessorFunction[]

  // let activeProcessors: Processor[]
  // let enabledProcessors: {[name: string]: boolean} = {}

  // let processorOptions: Record<string, any> = {}
  // for (const processor of allProcessors) {
  //   enabledProcessors[processor.name] = defaultProcessorFunctions.includes(processor.function)
  //   for (const optionSpec of processor.optionsSpec) {
  //     processorOptions[optionSpec.name] = optionSpec.value.default
  //   }
  // }

  const config = derived([viewOptionsCallStack], ([viewOptionsCallStack]) => {
    const processors = [
      viewOptionsCallStack.hideImportlib ? remove_importlib : null,
      viewOptionsCallStack.hideTracebackHide ? remove_tracebackhide : null,
      merge_consecutive_self_time,
      aggregate_repeated_calls,
      remove_unnecessary_self_time_nodes,
      viewOptionsCallStack.hideIrrelevant ? remove_irrelevant_nodes : null,
      viewOptionsCallStack.hidePyinstrument ? remove_first_pyinstrument_frames_processor : null,
      viewOptionsCallStack.collapseMode !== 'disabled' ? group_library_frames_processor : null,
    ].filter(p => p !== null)
    const options = {}
    return {processors, options}
  })

  // let config: {processors: ProcessorFunction[], options: ProcessorOptions}
  // $: config = computeProcessorsAndOptions()
  // $: activeProcessors = defaultProcessorFunctions.map(f => allProcessors.find(p => p.function == f)!).filter(p => enabledProcessors[p.name])

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
