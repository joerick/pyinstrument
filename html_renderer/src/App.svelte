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
  favicon.rel = 'shortcut icon'
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

  const rootFrame = session.rootFrame;
  const duration = rootFrame?.time.toLocaleString(undefined, {maximumSignificantDigits: 3});
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
  <div class="header">
    <Header session={session} />
  </div>
  <div class="body">
    {#if !session.rootFrame}
      <div class="margins">
        <div class="spacer" style="height: 20px;"></div>
        <div class="error">
          No samples recorded.
        </div>
      </div>
    {:else if $viewOptions.viewMode === 'call-stack'}
      <CallStackView session={session} />
    {:else if $viewOptions.viewMode === 'timeline'}
      <TimelineView session={session} />
    {:else}
      <div class="error">
        Unknown view mode: {$viewOptions.viewMode}
      </div>
    {/if}
  </div>
</div>


<style lang="scss">
  .app {
    font-family: 'Source Sans Pro', Arial, Helvetica, sans-serif;
    font-size-adjust: 0.486;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }
  .body {
    flex: 1;
    position: relative;
  }
</style>
