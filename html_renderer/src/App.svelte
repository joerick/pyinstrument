<script lang="ts">
  import Header from './components/Header.svelte'
  import type Session from "./lib/model/Session";
  export let session: Session
  import faviconImage from './assets/favicon.png'
  import { onDestroy, onMount } from 'svelte';
  import TreeView from './components/TreeView.svelte';
  import Timeline from './components/Timeline.svelte';

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
  session.target_description = 'Block at /Users/joerick/Projects/pyinstrument/pyinstrument/console.py:80'
  let name
  // let name = rootFrame?.function;
  // if (name == '<module>') {
  //   name = session.target_description;
  // }

  let match
  // grab just the last path component of the description as a short version
  // for the page title
  if (match = /[^\s/]+(:\d+)?$/.exec(session.target_description)) {
    name = match[0]
  } else {
    name = session.target_description
  }

  document.title = `${duration}s - ${name} - pyinstrument`
</script>

<div class="app">
  <Header session={session} />
  <div class="spacer" style="height: 20px;"></div>
  <div class="margins">

    {#if !session.rootFrame}
      <div class="error">
        No samples recorded.
      </div>
    {:else}
      <TreeView session={session} />
      <Timeline session={session} />
    {/if}
  </div>
</div>


<style lang="scss">
  .app {
    font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  .program {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #B4B4B4;
    .label {
      color: #EAEAEA;
      text-transform: uppercase;
    }
  }
</style>
