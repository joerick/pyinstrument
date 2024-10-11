<script lang="ts">
  import { viewOptionsTimeline } from "../lib/settings";
  import { randomId } from "../lib/utils";
  const cid = randomId();
</script>

<div class="view-options-timeline">

  <div class="option-group">
    <div class="name">Remove frames</div>
    <div class="body">

      <div class="option">
        <input
          id={cid + "removeImportlib"}
          type="checkbox"
          bind:checked={$viewOptionsTimeline.removeImportlib}
        />
        <label for={cid + "removeImportlib"}> importlib machinery </label>
      </div>

      <div class="option">
        <input
          id={cid + "removeTracebackHide"}
          type="checkbox"
          bind:checked={$viewOptionsTimeline.removeTracebackHide}
        />
        <label for={cid + "removeTracebackHide"}>
          Frames declaring __traceback_hide__
        </label>
      </div>

      <div class="option">
        <input
          id={cid + "removePyinstrument"}
          type="checkbox"
          bind:checked={$viewOptionsTimeline.removePyinstrument}
        />
        <label for={cid + "removePyinstrument"}> pyinstrument frames </label>
      </div>
    </div>
  </div>
</div>

<style lang="scss">
  .view-options-timeline {
    padding: 6px 9px;
  }
</style>
