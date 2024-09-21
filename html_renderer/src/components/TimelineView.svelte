<script lang="ts">
  import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
  import type Session from "../lib/model/Session";
  import { applyProcessors } from "../lib/model/modelUtil";
  import { allProcessors, type Processor } from "../lib/model/processors";
  import * as processors from "../lib/model/processors";
  import TimelineCanvasView from "./TimelineCanvasView";

  export let session: Session

  const defaultProcessorFunctions = [
    processors.remove_importlib,
    processors.remove_tracebackhide,
    processors.remove_first_pyinstrument_frames_processor,
  ] as processors.ProcessorFunction[]
  const processorOptions = {}

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), defaultProcessorFunctions, processorOptions)

  let rootElement: HTMLDivElement|null = null
  let timelineCanvasView: TimelineCanvasView|null = null

  $: if (rootElement) {
    timelineCanvasView = new TimelineCanvasView(rootElement)
  }

  $: if (rootFrame && timelineCanvasView) {
    timelineCanvasView.setRootFrame(rootFrame)
  }
</script>

<div class="timeline" bind:this={rootElement}>

</div>

<style lang="scss">
  .timeline {
    position: relative;
    height: 800px;
  }
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
