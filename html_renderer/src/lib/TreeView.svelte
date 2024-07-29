<script lang="ts">
  import FrameView from './Frame.svelte'
  import type Frame from './model/Frame';
  import type Session from './model/Session';
  import {aggregate_repeated_calls, group_library_frames_processor, merge_consecutive_self_time, remove_first_pyinstrument_frames_processor, remove_importlib, remove_irrelevant_nodes, remove_tracebackhide, remove_unnecessary_self_time_nodes, type ProcessorFunction, type ProcessorOptions, allProcessors, type Processor} from './model/processors'
  export let session: Session

  const defaultProcessorFunctions = [
    remove_importlib,
    remove_tracebackhide,
    merge_consecutive_self_time,
    aggregate_repeated_calls,
    remove_unnecessary_self_time_nodes,
    remove_irrelevant_nodes,
    remove_first_pyinstrument_frames_processor,
    group_library_frames_processor,
  ] as ProcessorFunction[]

  let activeProcessors: Processor[]
  let enabledProcessors: {[name: string]: boolean} = {}

  let processorOptions: Record<string, any> = {}
  for (const processor of allProcessors) {
    enabledProcessors[processor.name] = defaultProcessorFunctions.includes(processor.function)
    for (const optionSpec of processor.optionsSpec) {
      processorOptions[optionSpec.name] = optionSpec.value.default
    }
  }

  $: activeProcessors = defaultProcessorFunctions.map(f => allProcessors.find(p => p.function == f)!).filter(p => enabledProcessors[p.name])

  function applyProcessors(rootFrame: Frame, processors: Processor[], options: ProcessorOptions) {
    let frame: Frame|null = rootFrame
    for (const processor of processors) {
      frame = processor.function(frame, options)
      if (!frame) {
        return null
      }
    }
    return frame
  }

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), activeProcessors, processorOptions)
</script>

<div class="tree-view">
  <div class="options">
    <h2>Options</h2>
    <div class="processor-options">
      {#each allProcessors as processor}
        <label>
          <input type="checkbox" bind:checked={enabledProcessors[processor.name]} />
          {processor.name}
        </label>
      {/each}
    </div>
    <!-- <div class="processor-options">
      {#each Object.keys(processorOptions) as optionName}
        <label>
          {optionName}
          <input type="text" bind:value={processorOptions[optionName]} />
        </label>
      {/each}
    </div> -->
  </div>
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
