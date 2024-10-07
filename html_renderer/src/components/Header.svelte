<script lang="ts">
  import type Session from "../lib/model/Session";
  import CogIcon from './CogIcon.svelte';
  import Logo from './Logo.svelte';
  import {viewOptions} from '../lib/settings'
  import ViewOptions from "./ViewOptions.svelte";
  import { htmlForStringWithWBRAtSlashes } from "../lib/utils";

  export let session: Session;

  const startTime = new Date(session.startTime*1000).toLocaleString(undefined, {dateStyle: 'long', timeStyle: 'medium'})
  const cpuUtilisation = session.cpuTime / session.duration

  let viewOptionsVisible = false

  function viewOptionsButtonClicked(event: MouseEvent) {
    viewOptionsVisible = !viewOptionsVisible
  }
</script>

<div class="header">
  <div class="margins">
    <div class="row">
      <div class="logo">
        <Logo />
      </div>
      <div class="layout">
        <div class="target-description">
          {@html htmlForStringWithWBRAtSlashes(session.target_description)}
        </div>
        <div class="metrics">
          <div class="metric date">
            <span class="metric-label">Recorded:</span>
            <span class="metric-value">{startTime}</span>
          </div>
          <br>
          <div class="metric">
            <span class="metric-label">Samples:</span>
            <span class="metric-value">{session.sampleCount}</span>
          </div>
          <div class="metric">
            <span class="metric-label">CPU utilization:</span>
            <span class="metric-value">{(cpuUtilisation * 100).toFixed(0)}%</span>
          </div>
        </div>
        <div class="view-options">
          <div class="toggle">
            View:
            <label>
              <input type="radio" bind:group={$viewOptions.viewMode} value="call-stack">
              Call stack
            </label>
            <label>
              <input type="radio" bind:group={$viewOptions.viewMode} value="timeline">
              Timeline
            </label>
          </div>
          <div class="spacer" style="flex: 1"></div>
          <div class="button-container">
            <button on:click|preventDefault|stopPropagation={viewOptionsButtonClicked} class="js-view-options-button">
              <CogIcon />
              View options
            </button>
            {#if viewOptionsVisible}
              <ViewOptions on:close={() => viewOptionsVisible = false}/>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<style lang="scss">
  .header {
    background: #292f32;
    font-size: 14px;
    padding: 9px 0;
  }
  .row {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .logo {
    margin: 0 -6px;
    margin-right: -3px;
  }
  .layout {
    flex: 1;
    display: grid;
    gap: 0 10px;
    grid-template-columns: auto minmax(auto, max-content);
  }
  @media (max-width: 800px) {
    .layout {
      grid-template-columns: 1fr;
    }
  }
  .target-description {
    font-weight: 600;
    margin-bottom: 1px;
  }
  .view-options {
    display: flex;
    flex-wrap: wrap;
    // margin-top: 2px;
    label {
      margin: 0 5px;
      white-space: nowrap;
    }
  }
  .metrics {
    grid-row: span 2;
    /* grid-gap: 1px 10px; */
    text-align: right;
    align-items: end;
    min-width: min-content;
  }
  @media (max-width: 800px) {
    .metrics {
      text-align: left;
      br {
        display: none;
      }
    }
  }
  .metric {
    display: inline-block;
    white-space: nowrap;
    margin-left: 2px;
  }
  @media (max-width: 800px) {
    .metric {
      margin-left: 0;
      margin-right: 2px;
    }
  }

  .metric-label {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.6);
  }
  .metric-value {
    color: rgba(255, 255, 255, 0.4);
  }
  input[type=radio] {
    // width: 10px;
    // height: 10px;
    // border: 1px solid currentColor;
    // background-color: transparent;
    vertical-align: -8%;
  }
  .button-container {
    // display: flex;
    position: relative;
  }
  button {
    $bg: #5C6063;
    background: $bg;
    border-radius: 6px;
    font: inherit;
    font-size: calc(12em/14);
    color: inherit;
    border: none;
    cursor: pointer;

    &:hover {
      background: lighten($color: $bg, $amount: 3);
    }
    &:active {
      background: darken($color: $bg, $amount: 3);
    }
  }
</style>
