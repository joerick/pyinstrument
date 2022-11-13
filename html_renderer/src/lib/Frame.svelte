<script lang="ts">
  import { timeFormat, visibleGroups } from './appState';
  import type Frame from './model/Frame'
  export let frame: Frame
  export let indent: number = 0

  let childrenVisible = true

  let isVisible: boolean
  $: {
    if (!frame.group) {
      isVisible = true
    } else if ($visibleGroups[frame.groupId ?? '']) {
      isVisible = true
    } else if (frame.group?.rootFrame === frame) {
      isVisible = true
    } else if (frame.children.filter(f => !f.group).length > 1) {
      isVisible = true
    } else {
      isVisible = false
    }
  }

  let name: string
  if (frame.className) {
    name = `${frame.className}.${frame.function}`
  } else {
    name = frame.function
  }

  const codePosition = `${frame.filePathShort}:${frame.lineNo.toString().padEnd(4, ' ')}`

  let formattedTime: string
  $: if ($timeFormat === "absolute") {
    formattedTime = frame.time.toLocaleString(undefined, {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3,
    });
  } else if ($timeFormat === 'proportion') {
    formattedTime = `${(frame.proportionOfTotal * 100).toLocaleString(undefined, {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1,
    })}%`;
  } else {
    throw new Error("unknown timeFormat");
  }

  let groupLibrarySummary: string|null = null
  if (frame.group) {
    const libraries = frame.group.libraries
    if (libraries.length < 4) {
      groupLibrarySummary = libraries.join(', ')
    } else {
      groupLibrarySummary = `${libraries[0]}, ${libraries[1]}, ${libraries[2]}...`
    }
  }

  let timeColor: string

  if (frame.proportionOfTotal > 0.6) {
    timeColor = '#FF4159'
  } else if (frame.proportionOfTotal > 0.3) {
    timeColor = '#F5A623'
  } else if (frame.proportionOfTotal > 0.2) {
    timeColor = '#D8CB2A'
  } else {
    timeColor = '#7ED321'
  }

  function descriptionClicked() {
    childrenVisible = !childrenVisible
  }

  $: isGroupVisible = $visibleGroups[frame.groupId ?? ''] === true

  function headerClicked() {
    visibleGroups.update(groups => ({
      ...groups,
      [frame.groupId ?? '']: !isGroupVisible
    }))
  }

</script>
<div class="frame">
  {#if isVisible}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="frame-description"
         class:application-code={frame.isApplicationCode}
         class:children-visible={childrenVisible}
         style:padding-left={`${indent*35}px`}
         on:click|preventDefault|stopPropagation="{descriptionClicked}">
      <div class="frame-triangle"
           class:rotate="{childrenVisible}"
           style:visibility="{frame.children.length > 0 ? 'visible' : 'hidden'}">
        <svg width="6" height="10"><path d="M.937-.016L5.793 4.84.937 9.696z" fill="{timeColor}" fill-rule="evenodd" fill-opacity=".582"/></svg>
      </div>
      <div class="time"
           style:color="{timeColor}"
           style:font-weight="{frame.proportionOfTotal < 0.2 ? 500 : 600}">
        {formattedTime}
      </div>
      <div class="name">{name}</div>
      <div class="spacer" style="flex: 1"></div>
      <div class="code-position">
        {codePosition}
      </div>
    </div>
  {/if}

  {#if frame.group && frame.group.rootFrame == frame && childrenVisible}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="group-header"
         style:padding-left={`${indent*35}px`}
         on:click|preventDefault|stopPropagation={headerClicked}>
      <div class="group-header-button">
        <div class="group-triangle" class:rotate={isGroupVisible}>
          <svg width="6" height="10"><path d="M.937-.016L5.793 4.84.937 9.696z" fill="#FFF" fill-rule="evenodd" fill-opacity=".582"/></svg>
        </div>
        {frame.group.frames.length} frames hidden
        ({groupLibrarySummary})
      </div>
    </div>
  {/if}

  {#if childrenVisible}
    {#each frame.children as child (child.identifier)}
      <svelte:self frame="{child}"
                   indent="{indent + (isVisible ? 1 : 0)}" />
    {/each}
  {/if}

  <div class="visual-guide"
       style:left={`${indent*35 + 21}px`}
       style:backgroundColor={timeColor}>
  </div>
</div>

<style lang="scss">
.frame {
  font-family: 'Source Code Pro', 'Roboto Mono', Consolas, Monaco, monospace;
  font-size: 15px;
  z-index: 0;
  position: relative;
  user-select: none;
}
.group-header {
  margin-left: 35px;
}
.group-header-button {
  display: inline-block;
  color: rgba(255, 255, 255, 0.58);
  user-select: none;
  cursor: default;
  position: relative;
}
.group-header-button::before {
  position: absolute;
  left: -3px;
  right: -3px;
  top: 0px;
  bottom: -1px;
  content: "";

  z-index: -1;
  background-color: #3b4043;
}
.group-header-button:hover::before {
  background-color: #4a4f54;
}
.group-triangle, .frame-triangle {
  width: 6px;
  height: 10px;
  padding-left: 6px;
  padding-right: 5px;
  display: inline-block;
}
.group-triangle.rotate, .frame-triangle.rotate {
  transform: translate(6px, 4px) rotate(90deg);
}

.frame-description {
  display: flex;
}
.frame-description:hover::before {
  position: absolute;
  left: -3px;
  right: -3px;
  top: -1px;
  height: 22px;
  content: "";

  z-index: -1;
  background-color: #354759;
  opacity: 0.5;
}
.frame-triangle {
  opacity: 1.0;
}
.frame-description.children-visible .frame-triangle {
  opacity: 0.0;
}
.frame-description.children-visible:hover .frame-triangle {
  opacity: 1.0;
}
.name, .time, .code-position {
  user-select: text;
  cursor: default;
}
.application-code .name {
  color: rgba(93, 179, 255, 1.0);
}
.time {
  margin-right: 0.55em;
  color: rgba(184, 233, 134, 0.52);
}
.code-position {
  color: rgba(255, 255, 255, 0.5);
  text-align: right;
  margin-left: 1em;
}

:global {
  .visual-guide {
    top: 21px;
    bottom: 0;
    left: 0;
    width: 2px;
    background-color: white;
    position: absolute;
    opacity: 0.08;
  }
  .frame-description:hover ~ .visual-guide {
    opacity: 0.4;
  }
  .frame-description:hover ~ .children .visual-guide {
    opacity: 0.1;
  }
}
</style>
