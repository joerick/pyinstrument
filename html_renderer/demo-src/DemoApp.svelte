<script lang="ts">
  import pyinstrumentHTMLRenderer from "../src/main";

  const fileURLs = import.meta.glob("../demo-data/*.json", {import: "default"})

  const files = Object.entries(fileURLs).map(([srcURL, promiseFn]) => {
    const filename = srcURL.split("/").pop()!;
    const stem = filename.split(".").slice(0, -1).join(".");
    return { name: stem, promiseFn };
  });

  let file = files[0];

  let data: any = null;
  let error: Error | null = null;
  let loading = false;
  $: {
    loading = true;
    error = null;
    data = null;
    file.promiseFn()
      .then((json) => {
        data = json;
        error = null;
      })
      .catch((e) => {
        error = e;
      })
      .finally(() => {
        loading = false;
      });
  }

  let appComponent: ReturnType<
    (typeof pyinstrumentHTMLRenderer)["render"]
  > | null = null;
  let resultElement: HTMLElement | undefined;

  $: if (resultElement && data) {
    if (appComponent) {
      appComponent.$destroy();
    }
    appComponent = pyinstrumentHTMLRenderer.render(resultElement, data);
  }
</script>

<div class="demo-app">
  <div class="header">
    <div class="left"></div>
    <div class="right">
      Choose a demo profile:
      <select bind:value={file}>
        {#each files as optionFile}
          <option value={optionFile}>{optionFile.name}</option>
        {/each}
      </select>
    </div>
  </div>
  <div class="body">
    {#if loading}
      <div>Loading...</div>
    {:else if error}
      <div>Error loading file: {error.message}</div>
    {/if}

    <div class="result-element" style={!data ? 'display: none' : ''} bind:this={resultElement}></div>
  </div>
</div>

<style lang="scss">
  .demo-app {
    background-color: #111;
    color: white;
    font-size: 11px;
    font-family:
      system-ui,
      -apple-system,
      BlinkMacSystemFont,
      "Segoe UI",
      Roboto,
      Oxygen,
      Ubuntu,
      Cantarell,
      "Open Sans",
      "Helvetica Neue",
      sans-serif;

    display: flex;
    flex-direction: column;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }
  .header {
    // background: #292f32;
    // font-size: 14px;
    padding: 5px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .body {
    position: relative;
    flex: 1;
  }
  select {
    font: inherit;
  }
</style>
