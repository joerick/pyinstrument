<script lang="ts">
  import {timeFormat} from './appState';
  import type Session from "./model/Session";

  export let session: Session;

  const startTime = new Date(session.startTime*1000).toLocaleString()

  const cpuTime = session.cpuTime?.toLocaleString(undefined, {maximumSignificantDigits: 3})
  const duration = session.duration.toLocaleString(undefined, {maximumSignificantDigits: 3})
</script>

<div class="header">
  <div class="margins">
    <div class="row">
      <div class="title">pyinstrument</div>
      <div class="metrics">
        <label class="metric-label" for="absolute">Absolute time</label>
        <input type="radio" bind:group={$timeFormat} value="absolute"
          id="absolute"
          name="time-format" checked>

        <div class="metric-label">Recorded:</div>
        <div class="metric-value">{startTime}</div>
        <div class="metric-label">Duration:</div>
        <div class="metric-value">{duration} seconds</div>

        <label class="metric-label" for="proportion">Proportional time</label>
        <input type="radio" bind:group={$timeFormat} value="proportion"
          id="proportion"
          name="time-format">

        <div class="metric-label">Samples:</div>
        <div class="metric-value">{session.sampleCount}</div>
        <div class="metric-label">CPU time:</div>
        <div class="metric-value">{cpuTime} seconds</div>
      </div>
    </div>
  </div>
</div>

<style>
  .header {
    background: #292f32;
  }
  .row {
    display: flex;
    align-items: center;
  }
  .title {
    font-size: 34px;
    padding-top: 20px;
    padding-bottom: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-right: 10px;
    flex: 1;
  }
  .metrics {
    display: grid;
    grid-template-columns: auto auto auto auto auto auto;
    font-size: 14px;
    text-transform: uppercase;
    grid-gap: 1px 8px;
  }

  .metric-label {
    font-weight: 600;
    color: #a9abad;
  }
  .metric-value {
    color: #737779;
    margin-right: 0.5em;
  }
</style>
