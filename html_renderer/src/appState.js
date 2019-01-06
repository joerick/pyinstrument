import Vue from 'vue';

class AppState {
  constructor() {
    this.visibleGroups = {}
  }

  isGroupVisible(group) {
    return this.visibleGroups[group.id] === true;
  }

  setGroupVisibility(group, visible) {
    Vue.set(this.visibleGroups, group.id, visible);
  }
}

const appState = new AppState()
export default appState;
