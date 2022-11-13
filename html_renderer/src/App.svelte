<script lang="ts">
  import Header from './lib/Header.svelte'
  import Frame from './lib/Frame.svelte'
  import type Session from "./lib/model/Session";
  export let session: Session
  import faviconImage from './assets/favicon.png'
  import { onDestroy, onMount } from 'svelte';

  // add favicon
  const favicon = document.createElement('link')
  favicon.rel = 'shortut icon'
  favicon.href = faviconImage
  document.head.appendChild(favicon)

  // don't let the body scroll up due to lack of content (when a tree is closed)
  // prevents the frames from jumping around when they are collapsed
  function didScroll() {
    document.body.style.minHeight = `${window.scrollY + window.innerHeight}px`;
  }
  onMount(() => {
    window.addEventListener('scroll', didScroll);
    didScroll();
  });
  onDestroy(() => {
    window.removeEventListener('scroll', didScroll);
  });

  const rootFrame = session.rootFrame;
  const duration = rootFrame?.time.toLocaleString(undefined, {maximumSignificantDigits: 3});
  let name = rootFrame?.function;
  if (name == '<module>') {
    name = session.program;
  }

  document.title = `${duration}s - ${name} - pyinstrument`
</script>

<div class="app">
  <Header session={session} />
  <div class="spacer" style="height: 20px;"></div>
  <div class="margins">
    {#if session.rootFrame}
      <Frame frame={session.rootFrame} />
    {:else}
      <div class="error">
        No samples recorded.
      </div>
    {/if}
  </div>
</div>


<style lang="scss">
  .app {
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
