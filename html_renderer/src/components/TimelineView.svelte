<script lang="ts">
  import { derived } from "svelte/store";
  import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
  import type Session from "../lib/model/Session";
  import { applyProcessors } from "../lib/model/modelUtil";
  import { viewOptionsTimeline } from "../lib/settings";
  import TimelineCanvasView from "./TimelineCanvasView";
  import { remove_first_pyinstrument_frames_processor, remove_importlib, remove_tracebackhide, type ProcessorOptions } from "../lib/model/processors";
  import { onDestroy } from "svelte";

  export let session: Session
  const config = derived([viewOptionsTimeline], ([viewOptionsTimeline]) => {
      const processors = [
        viewOptionsTimeline.removeImportlib ? remove_importlib : null,
        viewOptionsTimeline.removeTracebackHide ? remove_tracebackhide : null,
        viewOptionsTimeline.removePyinstrument ? remove_first_pyinstrument_frames_processor : null,
      ].filter(p => p !== null)
      const options = {} as ProcessorOptions
      return {processors, options}
    })

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), $config.processors, $config.options)

  let rootElement: HTMLDivElement|null = null
  let timelineCanvasView: TimelineCanvasView|null = null

  $: if (rootElement) {
    timelineCanvasView = new TimelineCanvasView(rootElement)
  }
  onDestroy(() => {
    timelineCanvasView?.destroy()
  })

  $: if (rootFrame && timelineCanvasView) {
    timelineCanvasView.setRootFrame(rootFrame)
  }
</script>

<div class="timeline" bind:this={rootElement}>

</div>

<style lang="scss">
  .timeline {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: hidden;
    user-select: none;
  }
</style>
