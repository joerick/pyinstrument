<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { viewOptions } from "../lib/settings";
  import ViewOptionsCallStack from "./ViewOptionsCallStack.svelte";
  import ViewOptionsTimeline from "./ViewOptionsTimeline.svelte";
  import { onClickOutside } from "../lib/utils";

  const dispatch = createEventDispatcher();
  function clickOutside() {
    dispatch("close");
  }
  let rootElement: HTMLElement | undefined;
  let boxElement: HTMLElement | undefined;
  onMount(() => {
    if (!boxElement) return;
    return onClickOutside(boxElement, clickOutside, {ignore: [".js-view-options-button"]});
  })
  function ensureBoxIsOnScreen() {
    // small screens might have the box off-screen
    if (!rootElement || !boxElement) return;
    const rootRect = rootElement.getBoundingClientRect();
    const boxRect = boxElement.getBoundingClientRect();
    const boxWidth = boxRect.width;
    if (rootRect.right - boxWidth - 20 < 0) {
      boxElement.style.right = `${rootRect.right - boxWidth - 20}px`;
    } else {
      boxElement.style.right = "0";
    }
  }
  onMount(() => {
    ensureBoxIsOnScreen();
    window.addEventListener("resize", ensureBoxIsOnScreen);
    return () => window.removeEventListener("resize", ensureBoxIsOnScreen);
  });

  let title = "View options";
  $: if ($viewOptions.viewMode === "call-stack") {
    title = "Call stack view options";
  } else if ($viewOptions.viewMode === "timeline") {
    title = "Timeline view options";
  }
</script>

<div class="view-options" bind:this={rootElement}>
  <div class="box" bind:this={boxElement}>
    <div class="title-row">{title}</div>
    <div class="body">
      {#if $viewOptions.viewMode === "call-stack"}
        <ViewOptionsCallStack />
      {:else if $viewOptions.viewMode === "timeline"}
        <ViewOptionsTimeline />
      {/if}
    </div>
  </div>
</div>

<style lang="scss">
  .view-options {
    position: absolute;
    z-index: 1;
    right: 0;
  }
  .box {
    width: 90vw;
    max-width: 282px;
    height: max-content;
    max-height: calc(100vh - 100px);
    position: absolute;
    right: 0;
    top: calc(100% + 4px);
    border-radius: 5px;
    border: 1px solid #4e5255;
    background: #2a2f32;
    box-shadow: 0px 2px 14px -5px rgba(0, 0, 0, 0.25);
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .title-row {
    padding: 5px 9px;
    font-size: 12px;
    font-weight: 600;
    background-color: #3c4144;
  }
  .body {
    overflow-y: auto;
    flex-basis: content;
    flex-shrink: 1;
  }
</style>
