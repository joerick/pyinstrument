<script lang="ts">
  import FrameView from './Frame.svelte'
  import type Frame from '../lib/model/Frame';
  import type Session from '../lib/model/Session';
  import { applyProcessors } from '../lib/model/modelUtil';
  import {aggregate_repeated_calls, group_library_frames_processor, merge_consecutive_self_time, remove_first_pyinstrument_frames_processor, remove_importlib, remove_irrelevant_nodes, remove_tracebackhide, remove_unnecessary_self_time_nodes, type ProcessorFunction, type ProcessorOptions, allProcessors, type Processor, remove_useless_groups_processor} from '../lib/model/processors'
  export let session: Session
  import { viewOptionsCallStack } from '../lib/settings';
  import { derived } from 'svelte/store';
  import { onMount } from 'svelte';

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
      remove_useless_groups_processor,
    ].filter(p => p !== null)
    const options = {
      filterThreshold: viewOptionsCallStack.removeIrrelevantThreshold,
      hideRegex: viewOptionsCallStack.collapseMode == 'custom' ? viewOptionsCallStack.collapseCustomHide : undefined,
      showRegex: viewOptionsCallStack.collapseMode == 'custom' ? viewOptionsCallStack.collapseCustomShow : undefined,
    } as ProcessorOptions
    return {processors, options}
  })

  let element: HTMLElement|undefined
  let scrollInnerElement: HTMLElement|undefined
  let scrollSizeFixerElement: HTMLElement|undefined
  // don't let the body scroll up due to lack of content (when a tree is
  // closed)
  //
  // the scrollSizeFixerElement prevents the frames from jumping around
  // when they are collapsed
  onMount(() => {
    let scrollMaxY = 0
    const el = element
    if (!el) { throw new Error('element not set'); }
    if (!scrollInnerElement) { throw new Error('scrollInnerElement not set'); }
    if (!scrollSizeFixerElement) { throw new Error('scrollSizeFixerElement not set'); }

    const sizeObserver = new ResizeObserver(() => {
      // when the size of the scrollInnerElement changes, we can increase the
      // scrollMaxY, but not decrease it
      const height = scrollInnerElement!.getBoundingClientRect().height;
      if (height > scrollMaxY) {
        scrollMaxY = height;
        scrollSizeFixerElement!.style.top = `${scrollMaxY-1}px`;
      }
    });
    sizeObserver.observe(scrollInnerElement!);
    let scrollListener
    el.addEventListener('scroll', scrollListener = () => {
      // when the user scrolls, we can decrease the scrollMaxY, but no smaller
      // than the current height of the scrollInnerElement
      let scrollBottom = el.scrollTop + el.clientHeight;
      const height = scrollInnerElement!.getBoundingClientRect().height;
      if (scrollBottom < height) {
        scrollBottom = height;
      }
      if (scrollBottom < scrollMaxY) {
        scrollMaxY = scrollBottom
        scrollSizeFixerElement!.style.top = `${scrollMaxY-1}px`;
      }
    });
    scrollListener();
    return () => {
      sizeObserver.disconnect();
      el.removeEventListener('scroll', scrollListener);
    }
  });

  let rootFrame: Frame|null
  $: rootFrame = applyProcessors(session.rootFrame.cloneDeep(), $config.processors, $config.options)
</script>

<div class="call-stack-view" bind:this={element}>
  <div class="scroll-inner" bind:this={scrollInnerElement}>
    {#if !rootFrame}
      <div class="margins">
        <div class="error">
          All frames were filtered out.
        </div>
      </div>
    {:else}
      <div class="call-stack-margins">
        <FrameView frame={rootFrame} rootFrame={rootFrame} />
      </div>
    {/if}
  </div>
  <div class="scroll-size-fixer" bind:this={scrollSizeFixerElement}></div>
</div>

<style lang="scss">
  .call-stack-view {
    background-color: #303538;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    overflow: auto;
    &:focus {
      outline: none;
    }
  }
  .scroll-inner {
    padding-top: 10px;
    padding-bottom: 40px;
    box-sizing: border-box;
    width: auto;
    min-width: max-content;
  }
  .call-stack-margins {
    padding-left: 18px;
    padding-right: 18px;
  }
  .scroll-size-fixer {
    height: 1px;
    width: 100px;
    position: absolute;
    left: 0;
    // background-color: red;
  }
</style>
