<script lang="ts">
  import { derived } from "svelte/store";
  import Frame, { SELF_TIME_FRAME_IDENTIFIER } from "../lib/model/Frame";
  import type Session from "../lib/model/Session";
  import { applyProcessors } from "../lib/model/modelUtil";
  import { viewOptionsTimeline } from "../lib/settings";
  import TimelineCanvasView from "./TimelineCanvasView";
  import { remove_first_pyinstrument_frames_processor, remove_importlib, remove_tracebackhide, type ProcessorOptions } from "../lib/model/processors";
  import { onDestroy } from "svelte";
  import { randomId } from "../lib/utils";

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
  $: rootFrame = applyProcessors(session.rootFrame?.cloneDeep() ?? null, $config.processors, $config.options)

  let rootElement: HTMLDivElement|null = null
  let timelineCanvasView: TimelineCanvasView|null = null
  const searchId = randomId()
  let searchQuery = ''
  let matchCount = 0

  $: if (rootElement) {
    timelineCanvasView = new TimelineCanvasView(rootElement)
  }
  onDestroy(() => {
    timelineCanvasView?.destroy()
  })

  $: if (rootFrame && timelineCanvasView) {
    timelineCanvasView.setRootFrame(rootFrame)
  }

  $: if (rootFrame && timelineCanvasView) {
    matchCount = timelineCanvasView.setSearchQuery(searchQuery)
  }
</script>

<div class="timeline-view">
  <div class="search-bar" role="search" aria-label="Timeline">
    <label for={searchId}>Find function</label>
    <input
      id={searchId}
      type="search"
      placeholder="Function or class name"
      bind:value={searchQuery}
      on:keydown={(event) => {
        if (event.key === 'Escape') {
          searchQuery = ''
          event.preventDefault()
        }
      }}
    />
    {#if searchQuery}
      <button on:click={() => searchQuery = ''}>Clear</button>
    {/if}
    <span class="match-count" role="status">
      {#if searchQuery.trim()}
        {matchCount} {matchCount === 1 ? 'match' : 'matches'}
      {/if}
    </span>
  </div>
  <div class="timeline" bind:this={rootElement}></div>
</div>

<style lang="scss">
  .timeline-view {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    display: flex;
    flex-direction: column;
  }
  .search-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px 12px;
    background: #212325;
    border-bottom: 1px solid #424547;
    color: #eee;
    font-size: 14px;

    input {
      min-width: 100px;
      max-width: 320px;
      flex: 1;
      padding: 4px 7px;
      background: #303336;
      border: 1px solid #62666a;
      border-radius: 3px;
      color: inherit;
      font: inherit;
    }
    button {
      color: inherit;
      font: inherit;
      background: transparent;
      border: 1px solid #62666a;
      border-radius: 3px;
      cursor: pointer;
    }
    .match-count {
      color: #ccc;
      min-width: 65px;
    }
  }
  .timeline {
    position: relative;
    flex: 1;
    min-height: 0;
    overflow: hidden;
    user-select: none;
  }
</style>
