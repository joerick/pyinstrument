<script lang="ts">
  import {timeFormat} from '../lib/appState';
  import type Session from "../lib/model/Session";
  import CogIcon from './CogIcon.svelte';
  import Logo from './Logo.svelte';

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
      <div class="left">
        <div class="target-description">
          {session.target_description}
        </div>
        <div class="view-options">
          <div class="toggle">
            View:
            <label>
              <input type="radio">
              Call stack
            </label>
            <label>
              <input type="radio">
              Timeline
            </label>
          </div>
          <div class="spacer" style="flex: 1"></div>
          <button on:click|preventDefault|stopPropagation={viewOptionsButtonClicked}>
            <CogIcon />
            Options
          </button>
        </div>
      </div>
      <div class="metrics">
        <div class="metric date">
          <span class="metric-label">Recorded:</span>
          <span class="metric-value">{startTime}</span>
        </div>
        <div class="metric">
          <span class="metric-label">Samples:</span>
          <span class="metric-value">{session.sampleCount}</span>
        </div>
        <div class="metric">
          <span class="metric-label">CPU utilization:</span>
          <span class="metric-value">{(cpuUtilisation * 100).toFixed(0)}%</span>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .header {
    background: #292f32;
    font-size: 14px;
  }
  .row {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .logo {
    position: relative;
    left: -6px;
  }
  .left {
    flex-grow: 1;
  }
  .target-description {
    font-weight: 600;
  }
  .view-options {
    display: flex;;
  }
  .metrics {
    display: grid;
    grid-template-columns: auto auto;
    grid-gap: 1px 10px;
    text-align: right;
    align-items: end;
  }
  .metric.date {
    grid-column: 1 / 3;
  }

  .metric-label {
    font-weight: 600;
    color: rgba(255, 255, 255, 0.6);
  }
  .metric-value {
    color: rgba(255, 255, 255, 0.4);
  }
  input[type=radio] {
    width: 10px;
    height: 10px;
    border: 1px solid currentColor;
    background-color: transparent;
  }
  button {
    background: #5C6063;
    border-radius: 6px;
    font: inherit;
    font-size: calc(12em/14);
    color: inherit;
    border: none;

  }
</style>
