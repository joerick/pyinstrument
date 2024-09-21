<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  import { viewOptions } from "../lib/settings";
  import ViewOptionsCallStack from "./ViewOptionsCallStack.svelte";
  import ViewOptionsTimeline from "./ViewOptionsTimeline.svelte";

  const dispatch = createEventDispatcher();
  function clickOutside() {
    dispatch("close");
  }
  let element: HTMLElement | undefined;
  onMount(() => {
    if (!element) return
    let clickListener;
    let pointerDownListener;

    let pointerId: number | undefined;
    element.addEventListener(
      "pointerdown",
      (pointerDownListener = (e: PointerEvent) => {
        pointerId = e.pointerId;
      }),
      { capture: true },
    );
    window.addEventListener(
      "click",
      (clickListener = (e: MouseEvent) => {
        console.log(e)
        if ('pointerId' in e && e.pointerId !== pointerId) {
          // this click didn't start in the element
          return;
        }
        if (!e.composedPath().includes(element!)) {
          clickOutside();
        }
      }),
      { capture: true },
    );
    return () => {
      window.removeEventListener("click", clickListener);
    };
  });

  let title = "View options";
  $: if ($viewOptions.viewMode === "call-stack") {
    title = "Call stack view options";
  } else if ($viewOptions.viewMode === "timeline") {
    title = "Timeline view options";
  }
</script>

<div class="view-options">
  <!-- <div class="backdrop" on:click|capture|preventDefault={backdropClicked} role="presentation"></div> -->
  <div class="box" bind:this={element}>
    <div class="title">{title}</div>
    {#if $viewOptions.viewMode === "call-stack"}
      <ViewOptionsCallStack />
    {:else if $viewOptions.viewMode === "timeline"}
      <ViewOptionsTimeline />
    {/if}
  </div>
</div>

<style lang="scss">
  .view-options {
    position: absolute;
    z-index: 1;
    right: 0;
  }
  .backdrop {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.1);
  }
  .box {
    width: 90vw;
    max-width: 282px;
    position: absolute;
    right: 0;
    top: calc(100% + 4px);
    border-radius: 5px;
    border: 1px solid #4e5255;
    background: #2a2f32;
    box-shadow: 0px 2px 14px -5px rgba(0, 0, 0, 0.25);
    overflow: hidden;
  }
  .title {
    padding: 5px 9px;
    font-size: 12px;
    font-weight: 600;
    background-color: #3c4144;
  }
</style>
