import Vue from 'vue';

class AppState {
  constructor() {
    this.visibleGroups = {};
    this.timeFormat = "absolute";
  }

  isGroupVisible(group) {
    return this.visibleGroups[group.id] === true;
  }

  setGroupVisibility(group, visible) {
    Vue.set(this.visibleGroups, group.id, visible);
  }

  setTimeFormat(timeFormat) {
    this.timeFormat = timeFormat;
  }
}

const appState = new AppState()
export default appState;
