<script lang="ts" context="module">
  // focusable code taken from https://stackoverflow.com/a/35173443/382749
  function getFocusableElements() {
    const FOCUSSABLE_ELEMENTS =
      'a:not([disabled]), button:not([disabled]), input[type=text]:not([disabled]), [tabindex]:not([disabled]):not([tabindex="-1"])';
    const callStackElement = document.querySelector('.call-stack-view')
    if (!callStackElement) throw new Error('callStackElement not found')

    var focussable = Array.prototype.filter.call(
      callStackElement.querySelectorAll(FOCUSSABLE_ELEMENTS),
      function (element) {
        //check for visibility while always include the current activeElement
        return (
          element.offsetWidth > 0 ||
          element.offsetHeight > 0 ||
          element === document.activeElement
        );
      },
    );
    return focussable;
  }
  function focusNextElement() {
    const focussable = getFocusableElements();

    var index = focussable.indexOf(document.activeElement);
    if (index > -1) {
      var nextElement = focussable[index + 1];
      if (nextElement) {
        nextElement.focus();
      }
    }
  }
  function focusPreviousElement() {
    const focussable = getFocusableElements();

    var index = focussable.indexOf(document.activeElement);
    if (index > -1) {
      var prevElement = focussable[index - 1];
      if (prevElement) {
        prevElement.focus();
      }
    }
  }
</script>

<script lang="ts">
  import { visibleGroups, collapsedFrames } from "../lib/appState";
  import { colorForFrameProportionOfTotal } from "../lib/color";
  import type Frame from "../lib/model/Frame";
  import { viewOptionsCallStack } from "../lib/settings";
  export let frame: Frame;
  export let rootFrame: Frame;
  export let indent: number = 0;

  let isVisible: boolean;
  $: {
    if (!frame.group) {
      isVisible = true;
    } else if ($visibleGroups[frame.group.id ?? ""]) {
      isVisible = true;
    } else if (frame.group?.rootFrame === frame) {
      isVisible = true;
    } else if (frame.children.filter((f) => !f.group).length > 1) {
      isVisible = true;
    } else {
      isVisible = false;
    }
  }

  const frameProportionOfTotal = frame.time / rootFrame.time;

  let name: string;

  $: if (frame.className) {
    name = `${frame.className}.${frame.function}`;
  } else {
    name = frame.function;
  }

  let codePosition: string
  if (frame.isSynthetic) {
    codePosition = "";
  } else if (frame.filePathShort == null) {
    codePosition = "";
  } else if (frame.lineNo == null || frame.lineNo === 0) {
    codePosition = frame.filePathShort;
  } else {
    codePosition = `${frame.filePathShort}:${frame.lineNo}`;
  }

  let formattedTime: string;
  $: if ($viewOptionsCallStack.timeFormat === "absolute") {
    formattedTime = frame.time.toLocaleString(undefined, {
      minimumFractionDigits: 3,
      maximumFractionDigits: 3,
    });
  } else if ($viewOptionsCallStack.timeFormat === "proportion") {
    formattedTime = `${(frameProportionOfTotal * 100).toLocaleString(
      undefined,
      {
        minimumFractionDigits: 1,
        maximumFractionDigits: 1,
      },
    )}%`;
  } else {
    throw new Error("unknown timeFormat");
  }

  let groupLibrarySummary: string | null = null;
  if (frame.group) {
    const libraries = frame.group.libraries;
    if (libraries.length < 4) {
      groupLibrarySummary = libraries.join(", ");
    } else {
      groupLibrarySummary = `${libraries[0]}, ${libraries[1]}, ${libraries[2]}...`;
    }
  }

  let timeColor: string;
  timeColor = colorForFrameProportionOfTotal(frameProportionOfTotal);

  function descriptionClicked(event: MouseEvent | KeyboardEvent) {
    setCollapsed(frame, !collapsed, event.altKey);
  }

  $: isGroupVisible = $visibleGroups[frame.group?.id ?? ""] === true;
  $: collapsed = $collapsedFrames[frame.uuid] === true;

  function setCollapsed(
    frame: Frame,
    value: boolean,
    recursive: boolean = true,
  ) {
    collapsedFrames.update((collapsedFrames) => ({
      ...collapsedFrames,
      [frame.uuid]: value,
    }));

    if (recursive) {
      for (const child of frame.children) {
        setCollapsed(child, value, true);
        if (frame.group && frame.group.rootFrame == frame) {
          setGroupVisible(frame.group.id, !value);
        }
      }
    }
  }

  function setGroupVisible(groupId: string, value: boolean) {
    visibleGroups.update((groups) => ({
      ...groups,
      [groupId]: value,
    }));
  }

  function groupHeaderClicked() {
    if (!frame.group) {
      return;
    }
    setGroupVisible(frame.group.id, !isGroupVisible);
  }
  function onKeydown(event: KeyboardEvent) {
    let wasHandled = true;
    if (event.key === "Enter" || event.key === " ") {
      descriptionClicked(event);
    } else if (event.key === "ArrowLeft" && !collapsed) {
      setCollapsed(frame, true, event.altKey);
    } else if (event.key === "ArrowRight" && collapsed) {
      setCollapsed(frame, false, event.altKey);
    } else if (event.key === "ArrowUp") {
      focusPreviousElement();
    } else if (event.key === "ArrowDown") {
      focusNextElement();
    } else {
      wasHandled = false;
    }

    if (wasHandled) {
      event.preventDefault();
      event.stopPropagation();
    }
  }
  function onGroupHeaderKeydown(event: KeyboardEvent) {
    let wasHandled = true;
    if (event.key === "Enter" || event.key === " ") {
      groupHeaderClicked();
    } else if (event.key === "ArrowLeft" && frame.group) {
      setGroupVisible(frame.group.id, false);
    } else if (event.key === "ArrowRight" && frame.group) {
      setGroupVisible(frame.group.id, true);
    } else if (event.key === "ArrowUp") {
      focusPreviousElement();
    } else if (event.key === "ArrowDown") {
      focusNextElement();
    } else {
      wasHandled = false;
    }

    if (wasHandled) {
      event.preventDefault();
      event.stopPropagation();
    }
  }
</script>

<div class="frame">
  {#if isVisible}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="frame-description"
      class:application-code={frame.isApplicationCode}
      class:children-visible={!collapsed}
      style:padding-left={`${indent * 35}px`}
      role="button"
      tabindex="0"
      on:keydown={onKeydown}
      on:click|preventDefault|stopPropagation={descriptionClicked}
    >
      <div
        class="frame-triangle"
        class:rotate={!collapsed}
        style:visibility={frame.children.length > 0 ? "visible" : "hidden"}
      >
        <svg width="6" height="10"
          ><path
            d="M.937-.016L5.793 4.84.937 9.696z"
            fill={timeColor}
            fill-rule="evenodd"
            fill-opacity=".582"
          /></svg
        >
      </div>
      <div
        class="time"
        style:color={timeColor}
        style:font-weight={frameProportionOfTotal < 0.15 ? 500 : 600}
      >
        {formattedTime}
      </div>
      <div class="name">{name}</div>
      <div class="code-position">
        {codePosition}
      </div>
    </div>

    <div
      class="visual-guide"
      style:left={`${indent * 35 + 21}px`}
      style:background-color={timeColor}
    ></div>
  {/if}

  {#if frame.group && frame.group.rootFrame == frame && !collapsed}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="group-header"
      style:padding-left={`${indent * 35}px`}
      role="button"
      tabindex="0"
      on:keydown={onGroupHeaderKeydown}
      on:click|preventDefault|stopPropagation={groupHeaderClicked}
    >
      <div class="group-header-button">
        <div class="group-triangle" class:rotate={isGroupVisible}>
          <svg width="6" height="10"
            ><path
              d="M.937-.016L5.793 4.84.937 9.696z"
              fill="#FFF"
              fill-rule="evenodd"
              fill-opacity=".582"
            /></svg
          >
        </div>
        {frame.group.frames.length-1} frames hidden ({groupLibrarySummary})
      </div>
    </div>
  {/if}

  {#if !collapsed && frame.children.length > 0}
    <div class="children">
      {#each frame.children as child (child.uuid)}
        <svelte:self
          frame={child}
          {rootFrame}
          indent={indent + (isVisible ? 1 : 0)}
        />
      {/each}
    </div>
  {/if}
</div>

<style lang="scss">
  .frame {
    font-family: "Source Code Pro", "Roboto Mono", Consolas, Monaco, monospace;
    font-size-adjust: 0.486094;
    font-size: 14px;
    z-index: 0;
    position: relative;
    user-select: none;
  }
  .group-header {
    user-select: none;
  }
  .group-header-button {
    margin-left: 35px;
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
    bottom: 0px;
    content: "";

    z-index: -1;
    background-color: #3b4043;
  }
  .group-header-button:hover::before {
    background-color: #4a4f54;
  }
  .group-triangle,
  .frame-triangle {
    width: 6px;
    height: 10px;
    padding-left: 6px;
    padding-right: 5px;
    display: inline-block;
  }
  .group-triangle.rotate,
  .frame-triangle.rotate {
    transform: translate(6px, 4px) rotate(90deg);
  }

  .frame-description {
    display: flex;
    white-space: nowrap;
  }
  .frame-description:hover {
    background-color: #35475980;
  }
  .frame-description:focus-visible,
  .group-header:focus-visible {
    outline: none;
    background-color: #37516c;
  }
  .frame-triangle {
    opacity: 1;
  }
  .frame-description.children-visible .frame-triangle {
    opacity: 0;
  }
  .frame-description.children-visible:hover .frame-triangle,
  .frame-description.children-visible:focus-visible .frame-triangle {
    opacity: 1;
  }
  .name,
  .time,
  .code-position {
    user-select: text;
    cursor: default;
  }
  .application-code .name {
    color: rgba(93, 179, 255, 1);
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
    opacity: 0.15;
  }
</style>
