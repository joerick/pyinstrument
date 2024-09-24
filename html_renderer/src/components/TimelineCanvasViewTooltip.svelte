<script lang="ts">
  import { colorForFrameProportionOfTotal } from "../lib/color";
  import { htmlForStringWithWBRAtSlashes } from "../lib/utils";

  export let name: string
  export let time: number
  export let selfTime: number
  export let totalTime: number
  export let location: string
  export let locationColor: string

  let locationHTML
  $: locationHTML = htmlForStringWithWBRAtSlashes(location)

  let timeMode: 'time' | 'self' | 'both'
  $: if (selfTime == time) {
    timeMode = 'self'
  } else if (selfTime / time > 1e-3) {
    timeMode = 'both'
  } else {
    timeMode = 'time'
  }

  function formatTime(time: number) {
    const color = colorForFrameProportionOfTotal(time / totalTime)
    return `<span style="color: ${color}">${time.toFixed(3)}</span>`
  }
</script>

<div class="timeline-canvas-view-tooltip">
  <div class="name">{name}</div>
  {#if timeMode == 'both'}
    <div class="label">time</div>
    <div class="time-row">
      <div class="time-val">{@html formatTime(time)}</div>
      {#if (selfTime / time) > 1e-3 }
        <div class="label">self</div>
        <div class="time-val">{@html formatTime (selfTime)}</div>
      {/if}
    </div>
  {:else}
    <div class="label">{timeMode == 'self' ? 'self' : 'time'}</div>
    <div class="time-val">{@html formatTime(time)}</div>
  {/if}
  <div class="label">loc</div>
  <div class="location-row">
    <div class="location-color" style={`background: ${locationColor}`}></div>
    <div>{@html locationHTML}</div>
  </div>
</div>

<style lang="scss">
  .timeline-canvas-view-tooltip {
    width: max-content;
    max-width: 310px;
    border-radius: 2px;
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: #202325;
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);

    display: grid;
    grid-template-columns: minmax(auto, 33px) minmax(auto, 1fr);
    gap: 1px 0;

    padding: 4px 10px;
    padding-bottom: 7px;

    font-size: 13px;
    color: white;

    .name {
      grid-column: span 2;
    }
    .label {
      color: rgba(255, 255, 255, 0.5);
      margin-right: 8px;
    }
    .time-val {
      margin-right: 10px;
      font-weight: 600;
    }
    .time-row {
      display: flex;
      justify-content: start;
    }
  }
</style>
