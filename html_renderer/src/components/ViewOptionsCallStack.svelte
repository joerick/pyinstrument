<script lang="ts">
  import { viewOptionsCallStack } from "../lib/settings";
  const cid = Math.random().toString(36).substring(4);
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
        <label for={cid + "collapseModeAll"}>Non-application code</label>
        <div class="description">
          Application code is anything run from outside the Python home
          directory.
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
          Regex on the source file path
          <div class="mini-input-grid">
            <label for="collapseCustomHide">Hide</label>
            <input
              id="collapseCustomHide"
              type="text"
              bind:value={$viewOptionsCallStack.collapseCustomHide}
              placeholder=".*/lib/.*"
            />
            <label for="collapseCustomShow">Show</label>
            <input
              id="collapseCustomShow"
              type="text"
              bind:value={$viewOptionsCallStack.collapseCustomShow}
              placeholder="myproject"
            />
          </div>
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
    align-items: center;
    input {
      font-family: 'Source Code Pro', 'Roboto Mono', Consolas, Monaco, monospace;
      font-size-adjust: 0.486094;

      border-radius: 3px;
      background: #4E5255;
      padding: 1px 5px;
      font-size: 12px;
      border: 1px solid #4e5255;
      color: #ccc;
      &:focus-visible {
        outline: 1px solid #abb2b7;
        // outline-offset: 1px;;
      }
    }
  }
</style>
