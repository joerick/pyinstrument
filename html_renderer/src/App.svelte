<script lang="ts">
  import Header from './components/Header.svelte'
  import type Session from "./lib/model/Session";
  export let session: Session
  import faviconImage from './assets/favicon.png'
  import { onDestroy, onMount } from 'svelte';
  import CallStackView from './components/CallStackView.svelte';
  import TimelineView from './components/TimelineView.svelte';
  import { viewOptions } from './lib/settings';

  // add favicon
  const favicon = document.createElement('link')
  favicon.rel = 'shortut icon'
  favicon.href = faviconImage
  document.head.appendChild(favicon)

  // add webfont
  const link = document.createElement('link');
  link.rel = 'preload';
  link.as = 'style'
  link.onload = () => {
    // clever trick to make the css non-blocking, i don't want to wait on slow
    // connections to see a local page.
    // adapted from
    // https://stackoverflow.com/a/60477207/382749
    link.rel = 'stylesheet'
  }
  link.href = `https://fonts.googleapis.com/css?family=Source+Code+Pro:400,600|Source+Sans+Pro:400,600&display=swap`;
  document.head.appendChild(link);

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
    {#if !session.rootFrame}
      <div class="spacer" style="height: 20px;"></div>
      <div class="margins">
        <div class="error">
          No samples recorded.
        </div>
      </div>
    {:else if $viewOptions.viewMode === 'call-stack'}
      <CallStackView session={session} />
    {:else if $viewOptions.viewMode === 'timeline'}
      <TimelineView session={session} />
    {:else}
      Unknown view mode: {$viewOptions.viewMode}
    {/if}
</div>


<style lang="scss">
  .app {
    font-family: 'Source Sans Pro', Arial, Helvetica, sans-serif;
    font-size-adjust: 0.486;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
</style>
