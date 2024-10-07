<script lang="ts">
  import { viewOptionsCallStack } from "../lib/settings";
  import { randomId } from "../lib/utils";
  const cid = randomId();

  function removeIrrelevantThresholdPercent() {
    const num = $viewOptionsCallStack.removeIrrelevantThreshold * 100
    return num.toLocaleString(undefined, { maximumFractionDigits: 4 });
  }
  function removeIrrelevantThresholdPercentSet(event: Event & { currentTarget: EventTarget & HTMLInputElement; }) {
    $viewOptionsCallStack.removeIrrelevantThreshold = event.currentTarget.valueAsNumber / 100;
  }
</script>

<div class="view-options-call-stack">
  <div class="option-group">
    <div class="name">Collapse frames</div>
    <div class="body">
      <div class="option">
        <input
          id={cid + "collapseModeAll"}
          type="radio"
          bind:group={$viewOptionsCallStack.collapseMode}
          value="non-application"
        />
        <label for={cid + "collapseModeAll"}>Library code</label>
        <div class="description">
          Code run from the Python stdlib, a virtualenv, or a conda env will be collapsed.
        </div>
      </div>
      <div class="option">
        <input
          id={cid + "collapseModeCustom"}
          type="radio"
          bind:group={$viewOptionsCallStack.collapseMode}
          value="custom"
        />
        <label for={cid + "collapseModeCustom"}>Custom</label>
        <div class="description">
          Regex on the source file path.
          <div class="mini-input-grid">
            <label for="collapseCustomShow">Show</label>
            <input
              id="collapseCustomShow"
              type="text"
              bind:value={$viewOptionsCallStack.collapseCustomShow}
              placeholder="myproject"
              spellcheck="false"
              autocapitalize="off"
              autocomplete="off"
              autocorrect="off"
            />
            <label for="collapseCustomHide">Hide</label>
            <input
              id="collapseCustomHide"
              type="text"
              bind:value={$viewOptionsCallStack.collapseCustomHide}
              placeholder=".*/lib/.*"
              spellcheck="false"
              autocapitalize="off"
              autocomplete="off"
              autocorrect="off"
            />
          </div>
          If neither match, the library code rule is used.
        </div>
      </div>
      <div class="option">
        <input
          id={cid + "collapseModeDisabled"}
          type="radio"
          bind:group={$viewOptionsCallStack.collapseMode}
          value="disabled"
        />
        <label for={cid + "collapseModeDisabled"}>Disabled</label>
      </div>
    </div>
  </div>

  <div class="option-group">
    <div class="name">Remove frames</div>
    <div class="body">

      <div class="option">
        <input
          id={cid + "removeImportlib"}
          type="checkbox"
          bind:checked={$viewOptionsCallStack.removeImportlib}
        />
        <label for={cid + "removeImportlib"}> importlib machinery </label>
      </div>

      <div class="option">
        <input
          id={cid + "removeTracebackHide"}
          type="checkbox"
          bind:checked={$viewOptionsCallStack.removeTracebackHide}
        />
        <label for={cid + "removeTracebackHide"}>
          Frames declaring __traceback_hide__
        </label>
      </div>

      <div class="option">
        <input
          id={cid + "removePyinstrument"}
          type="checkbox"
          bind:checked={$viewOptionsCallStack.removePyinstrument}
        />
        <label for={cid + "removePyinstrument"}> pyinstrument frames </label>
      </div>

      <div class="option">
        <input
          id={cid + "removeIrrelevant"}
          type="checkbox"
          bind:checked={$viewOptionsCallStack.removeIrrelevant}
        />
        <span>
          <label for={cid + "removeIrrelevant"}> Frames with durations less than </label>
          <input
            type="number"
            value={removeIrrelevantThresholdPercent()}
            min="0"
            max="99"
            step="0.01"
            on:input={removeIrrelevantThresholdPercentSet}
            style="width: 4em;"
          />
          % of the total time
        </span>
      </div>
    </div>
  </div>

  <div class="option-group">
    <div class="name">Time format</div>
    <div class="body">
      <div class="option">
        <label>
          <input
            type="radio"
            bind:group={$viewOptionsCallStack.timeFormat}
            value="absolute"
          />
          Absolute time in seconds
        </label>
      </div>

      <div class="option">
        <label>
          <input
            type="radio"
            bind:group={$viewOptionsCallStack.timeFormat}
            value="proportion"
          />
          Percentage of the total run time
        </label>
      </div>
    </div>
  </div>
</div>

<style lang="scss">
  .view-options-call-stack {
    padding: 6px 9px;
  }
  .option {
    display: grid;
    grid-template-columns: auto 1fr;
    align-items: start;
    padding-left: 1px;
    margin-bottom: 3px;
    .description {
      font-size: 12px;
      color: #999;
      grid-column: 2/3;
    }
  }
  .option-group {
    margin-bottom: 10px;
    .name {
      margin-bottom: 4px;
    }
  }
  .mini-input-grid {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 5px;
    align-items: baseline;
    margin-top: 3px;
    margin-bottom: 2px;
    label {
      font-weight: 600;
    }
  }
  input {
    font-family: "Source Code Pro", "Roboto Mono", Consolas, Monaco, monospace;
    font-size-adjust: 0.486094;

    border-radius: 3px;
    background: #4e5255;
    padding: 1px 5px;
    font-size: 12px;
    border: 1px solid #4e5255;
    color: #ccc;
    &:focus-visible {
      outline: 1px solid #abb2b7;
      // outline-offset: 1px;;
    }
  }
  input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }
</style>
