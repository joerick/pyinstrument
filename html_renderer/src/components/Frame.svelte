<script lang="ts">
  import { visibleGroups, collapsedFrames } from '../lib/appState';
  import { colorForFrameProportionOfTotal } from '../lib/color';
  import type Frame from '../lib/model/Frame'
  import { viewOptionsCallStack } from '../lib/settings';
  export let frame: Frame
  export let rootFrame: Frame
  export let indent: number = 0

  let isVisible: boolean
  $: {
    if (!frame.group) {
      isVisible = true
    } else if ($visibleGroups[frame.group.id ?? '']) {
      isVisible = true
    } else if (frame.group?.rootFrame === frame) {
      isVisible = true
    } else if (frame.children.filter(f => !f.group).length > 1) {
      isVisible = true
    } else {
      isVisible = false
    }
  }

  const frameProportionOfTotal = frame.time / rootFrame.time

  let name: string

  $: if (frame.className) {
    name = `${frame.className}.${frame.function}`
  } else {
    name = frame.function
  }

  const codePosition = `${frame.filePathShort}:${frame.lineNo?.toString().padEnd(4, ' ')}`

  let formattedTime: string
  $: if ($viewOptionsCallStack.timeFormat === "absolute") {
    formattedTime = frame.time.toLocaleString(undefined, {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3,
    });
  } else if ($viewOptionsCallStack.timeFormat === 'proportion') {
    formattedTime = `${(frameProportionOfTotal * 100).toLocaleString(undefined, {
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
  timeColor = colorForFrameProportionOfTotal(frameProportionOfTotal)

  function descriptionClicked(event: MouseEvent) {
    setCollapsed(frame, !collapsed, event.altKey)
  }

  $: isGroupVisible = $visibleGroups[frame.group?.id ?? ''] === true
  $: collapsed = $collapsedFrames[frame.uuid] === true

  function setCollapsed(frame: Frame, value: boolean, recursive: boolean = true) {
    collapsedFrames.update(collapsedFrames => ({
      ...collapsedFrames,
      [frame.uuid]: value
    }))

    if (recursive) {
      for (const child of frame.children) {
        setCollapsed(child, value, true)
        if (frame.group && frame.group.rootFrame == frame) {
          setGroupVisible(frame.group.id, !value)
        }
      }
    }
  }

  function setGroupVisible(groupId: string, value: boolean) {
    visibleGroups.update(groups => ({
      ...groups,
      [groupId]: value
    }))
  }

  function headerClicked() {
    if (!frame.group) {
      return
    }
    setGroupVisible(frame.group.id, !isGroupVisible)
  }
</script>
<div class="frame">
  {#if isVisible}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div class="frame-description"
         class:application-code={frame.isApplicationCode}
         class:children-visible={!collapsed}
         style:padding-left={`${indent*35}px`}
         on:click|preventDefault|stopPropagation="{descriptionClicked}">
      <div class="frame-triangle"
           class:rotate="{!collapsed}"
           style:visibility="{frame.children.length > 0 ? 'visible' : 'hidden'}">
        <svg width="6" height="10"><path d="M.937-.016L5.793 4.84.937 9.696z" fill="{timeColor}" fill-rule="evenodd" fill-opacity=".582"/></svg>
      </div>
      <div class="time"
           style:color="{timeColor}"
           style:font-weight="{frameProportionOfTotal < 0.2 ? 500 : 600}">
        {formattedTime}
      </div>
      <div class="name">{name}</div>
      <div class="code-position">
        {codePosition}
      </div>
    </div>
  {/if}

  {#if frame.group && frame.group.rootFrame == frame && !collapsed}
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

  {#if !collapsed && frame.children.length > 0}
    <div class="children">
      {#each frame.children as child (child.uuid)}
        <svelte:self frame="{child}"
                     rootFrame="{rootFrame}"
                     indent="{indent + (isVisible ? 1 : 0)}" />
      {/each}
    </div>
  {/if}

  <div class="visual-guide"
       style:left={`${indent*35 + 21}px`}
       style:backgroundColor={timeColor}>
  </div>
</div>

<style lang="scss">
.frame {
  font-family: 'Source Code Pro', 'Roboto Mono', Consolas, Monaco, monospace;
  font-size-adjust: 0.486094;
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
  white-space: nowrap;
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
  margin-left: 2em;
}

.visual-guide {
  top: 21px;
  bottom: 0;
  left: 0;
  width: 2px;
  background-color: white;
  position: absolute;
  opacity: 0.08;
  pointer-events: none;
}
:global(.frame-description:hover) ~ .visual-guide {
  opacity: 0.4;
}
:global(.frame-description:hover) ~ .children :global(.visual-guide) {
  opacity: 0.1;
}
</style>
