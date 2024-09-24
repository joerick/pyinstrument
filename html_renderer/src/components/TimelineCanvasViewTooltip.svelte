<script context="module" lang="ts">
  import { get } from "svelte/store";

  export interface TooltipFrameInfo {
    name: string
    time: number
    selfTime: number
    totalTime: number
    location: string
    locationColor: string
  }
  function getTimeMode(f: TooltipFrameInfo) {
    if (f.selfTime == f.time) {
      return 'self'
    } else if (f.selfTime / f.time > 1e-3) {
      return 'both'
    } else {
      return 'time'
    }
  }
  export function estimateWidth(ctx: CanvasRenderingContext2D, f: TooltipFrameInfo) {
    ctx.font = FONT
    const timeWidth = getTimeMode(f) == 'both' ? 140 : 70
    const nameWidth = ctx.measureText(f.name).width
    const locationWidth = ctx.measureText(f.location).width + 46
    const padding = 10 + 10
    let width = Math.max(timeWidth, nameWidth, locationWidth) + padding
    if (width > 310) {
      width = 310
    }
    return width
  }
  const MAX_WIDTH = 310
  const FONT = '400 13px Source Sans Pro, sans-serif'
</script>

<script lang="ts">
  import { colorForFrameProportionOfTotal } from "../lib/color";
  import { htmlForStringWithWBRAtSlashes } from "../lib/utils";

  export let f: TooltipFrameInfo

  let locationHTML
  $: locationHTML = htmlForStringWithWBRAtSlashes(f.location)

  let timeMode: 'time' | 'self' | 'both'
  $: timeMode = getTimeMode(f)

  function formatTime(time: number) {
    const color = colorForFrameProportionOfTotal(time / f.totalTime)
    return `<span style="color: ${color}">${time.toFixed(3)}</span>`
  }
</script>

<div class="timeline-canvas-view-tooltip"
     style={`font: ${FONT}; max-width: ${MAX_WIDTH}px;`}>
  <div class="name">{f.name}</div>
  {#if timeMode == 'both'}
    <div class="label">time</div>
    <div class="time-row">
      <div class="time-val">{@html formatTime(f.time)}</div>
      {#if (f.selfTime / f.time) > 1e-3 }
        <div class="label">self</div>
        <div class="time-val">{@html formatTime (f.selfTime)}</div>
      {/if}
    </div>
  {:else}
    <div class="label">{timeMode == 'self' ? 'self' : 'time'}</div>
    <div class="time-val">{@html formatTime(f.time)}</div>
  {/if}
  <div class="label">loc</div>
  <div class="location-row">
    <div class="location-color" style={`background: ${f.locationColor}`}></div>
    {@html locationHTML}
  </div>
</div>

<style lang="scss">
  .timeline-canvas-view-tooltip {
    box-sizing: border-box;
    width: max-content;
    border-radius: 2px;
    border: 1px solid rgba(255, 255, 255, 0.09);
    background: #202325;
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);

    display: grid;
    grid-template-columns: minmax(auto, 33px) minmax(auto, 1fr);
    gap: 1px 0;

    padding: 4px 10px;
    padding-bottom: 7px;

    color: white;

    .name {
      grid-column: span 2;
      line-break: anywhere;
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
    .location-color {
      width: 9px;
      height: 9px;
      margin-right: 3px;
      border-radius: 2px;
      position: relative;
      display: inline-block;

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border: 1px solid #383838;
        mix-blend-mode: color-dodge;
        border-radius: 2px;
      }
    }
  }
</style>
