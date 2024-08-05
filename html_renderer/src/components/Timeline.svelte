<script lang="ts">
  import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
  import type Session from "../lib/model/Session";
  import { applyProcessors } from "../lib/model/modelUtil";
  import { allProcessors, type Processor } from "../lib/model/processors";
  import * as processors from "../lib/model/processors";

  export let session: Session

  const defaultProcessorFunctions = [
    processors.remove_importlib,
    processors.remove_tracebackhide,
    processors.remove_first_pyinstrument_frames_processor,
  ] as processors.ProcessorFunction[]

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

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), activeProcessors, processorOptions)

  interface DisplayFrame {
    startTime: number
    frame: Frame
    depth: number
  }
  const frames: DisplayFrame[] = []
  function collectFrames(frame: Frame, startTime: number, depth: number) {
    frames.push({frame, startTime, depth})
    let childStartTime = startTime
    for (const child of frame.children) {
      if (child.identifier !== SELF_TIME_FRAME_IDENTIFIER) {
        // we don't render self time frames
        collectFrames(child, childStartTime, depth + 1)
      }
      childStartTime += child.time
    }
  }
  $: if (rootFrame) {
    collectFrames(rootFrame, 0, 0)
  }
</script>

<div class="timeline">
  <div class="frames">
    {#each frames as {frame, startTime, depth}}
      <div class="frame"
           style:top={`${depth*21}px`}
           style:left={`${startTime*20000}px`}
           style:width={`${frame.time*20000}px`}>{frame.function}</div>
    {/each}
  </div>
</div>

<style lang="scss">
  .frames {
    position: relative;
    height: 500px;
  }
  .frame {
    position: absolute;
    background-color: green;
    border: 1px solid black;
    padding: 0 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>
