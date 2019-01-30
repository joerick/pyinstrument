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
      session: window.profileSession,
    }
  },
  mounted() {
    window.App = this;
    this.setFavicon(require('./assets/favicon.png'));

    if (!this.session) {
      // in dev mode, load a sample json.
      fetch('./sample.json')
        .then(response => response.json())
        .then(sample => {
          this.session = sample;
        })
        .catch(console.log)
    }

    this.scrollListener = () => this.didScroll()
    window.addEventListener('scroll', this.scrollListener, {passive: true});
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.scrollListener, {passive: true});
  },
  methods: {
    didScroll() {
      // don't let the body scroll up due to lack of content (when a tree is closed)
      // prevents the frames from jumping around when they are collapsed
      document.body.style.minHeight = `${window.scrollY + window.innerHeight}px`;
    },
    setFavicon(image) {
      var link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      // link.type = 'image/x-icon';
      link.rel = 'shortcut icon';
      link.href = image;
      document.getElementsByTagName('head')[0].appendChild(link);
    }
  },
  computed: {
    rootFrame() {
      if (this.session && this.session.root_frame) {
        return new FrameModel(this.session.root_frame)
      }
    }
  },
  watch: {
    session: {
      handler() {
        if (!this.session || !this.rootFrame) {
          document.title = 'Pyinstrument';
          return;
        }

        const rootFrame = this.rootFrame;
        const duration = rootFrame.time.toLocaleString({maximumDecimalDigits: 3});
        let name = rootFrame.function;
        if (name == '<module>') {
          name = this.session.program;
        }

        document.title = `${duration}s - ${name} - pyinstrument`
      },
      immediate: true,
    },
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
