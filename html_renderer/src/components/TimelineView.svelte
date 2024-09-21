<script lang="ts">
  import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
  import type Session from "../lib/model/Session";
  import { applyProcessors } from "../lib/model/modelUtil";
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
</style>
