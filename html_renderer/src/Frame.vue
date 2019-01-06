<template>
  <div class="frame">

    <div class="frame-description" v-if="isVisible"
         :class="{'application-code': frame.isApplicationCode,
                  'children-visible': childrenVisible}"
         :style="{paddingLeft: `${indent*35}px`}"
         @click.prevent.stop="childrenVisible = !childrenVisible">
      <div class="frame-triangle"
           :class="{rotate: childrenVisible}"
           :style="{visibility: frame.children.length > 0 ? 'visible': 'hidden'}">
        <svg width="6" height="10"><path d="M.937-.016L5.793 4.84.937 9.696z" :fill="timeStyle.color" fill-rule="evenodd" fill-opacity=".582"/></svg>
      </div>
      <div class="time"
           :style="timeStyle">
        {{formattedTime}}
      </div>
      <div class="name">{{frame.function}}</div>
      <div class="spacer" style="flex: 1"></div>
      <div class="code-position">
        {{codePosition}}
      </div>
    </div>

    <div v-if="frame.group && frame.group.rootFrame == frame && childrenVisible" 
         class="group-header"
         :style="{paddingLeft: `${indent*35}px`}"
         @click.prevent.stop="headerClicked">
      <div class="group-header-button">
        <div class="group-triangle" :class="{rotate: isGroupVisible}">
          <svg width="6" height="10"><path d="M.937-.016L5.793 4.84.937 9.696z" fill="#FFF" fill-rule="evenodd" fill-opacity=".582"/></svg>
        </div>
        {{frame.group.frames.length}} frames hidden
        ({{groupLibrarySummary}})
      </div>
    </div>

    <div class="children" v-if="childrenVisible">
      <Frame v-for="child in frame.children"
             :key="child.identifier" 
             :frame="child"
             :indent="indent + (isVisible ? 1 : 0)" />
    </div>

    <div class="visual-guide" 
         :style="{left: `${indent*35 + 21}px`, 
                  backgroundColor: timeStyle.color}">
    </div>
  </div>
</template>

<script>
import appState from './appState';

export default {
  name: 'Frame',
  props: {
    frame: {},
    indent: {default: 0},
  },
  data() {
    return {
      childrenVisible: true,
    }
  },
  methods: {
    headerClicked() {
      appState.setGroupVisibility(this.frame.group, !this.isGroupVisible)
    }
  },
  computed: {
    isVisible() {
      if (!this.frame.group) {
        return true;
      }
      if (appState.isGroupVisible(this.frame.group)) {
        return true;
      }
      if (this.frame.group.rootFrame === this.frame) {
        return true;
      }
      if (this.frame.children.filter(f => !f.group).length > 1) {
        return true;
      }
      return false;
    },
    isGroupVisible() {
      return appState.isGroupVisible(this.frame.group);
    },
    codePosition() {
      return `${this.frame.filePathShort}:${this.frame.lineNo.toString().padEnd(4, ' ')}`
    },
    formattedTime() {
      return this.frame.time.toLocaleString(undefined, {
        minimumFractionDigits: 3,
        maximumFractionDigits: 3,
      })
    },
    groupLibrarySummary() {
      if (!this.frame.group) {
        return
      }
      const libraries = this.frame.group.libraries;
      if (libraries.length < 4) {
        return libraries.join(', ')
      } else {
        return `${libraries[0]}, ${libraries[1]}, ${libraries[2]}...`;
      }
    },
    timeStyle() {
      let color = undefined;
      let fontWeight = undefined;

      if (this.frame.proportionOfTotal > 0.6) {
        color = '#FF4159';
        fontWeight = 600;
      } else if (this.frame.proportionOfTotal > 0.3) {
        color = '#F5A623'
        fontWeight = 600;
      } else if (this.frame.proportionOfTotal > 0.2) {
        color = '#D8CB2A'
        fontWeight = 600;
      } else if (this.frame.proportionOfTotal > 0.0) {
        color = '#7ED321'
        fontWeight = 500;
      }

      return {color, fontWeight}
    },
  },
}
</script>

<style scoped>
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
</style>

<style>
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
</style>
