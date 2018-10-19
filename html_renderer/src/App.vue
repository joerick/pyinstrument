<template>
  <div id="app">
    <Header :session="session" v-if="session" />
    <div class="spacer" style="height: 20px;"></div>
    <div class="margins">
      <Frame v-if="rootFrame"
             :frame="rootFrame" />
    </div>
  </div>
</template>

<script>
import Frame from './Frame.vue';
import Header from './Header.vue';
import FrameModel from './model/Frame';
import appState from './appState';

export default {
  name: 'app',
  data() {
    return {
      appState,
      session: window.profilerSession,
    }
  },
  mounted() {
    if (!this.session) {
      import('./sample.json').then(sample => {
        this.session = sample;
      })
    }
  },
  computed: {
    rootFrame() {
      if (this.session) {
        return new FrameModel(this.session.root_frame)
      }
    }
  },
  components: {
    Frame,
    Header,
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:400,600|Source+Sans+Pro:400,600');

html, body {
  background-color: #303538;
  color: white;
  padding: 0;
  margin: 0;
}

#app {
  font-family: 'Source Sans Pro', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.margins {
  padding: 0 30px;
}
</style>
