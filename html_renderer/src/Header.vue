<template>
  <div class="header">
    <div class="margins">
      <div class="row">
        <div class="title">pyinstrument</div>
        <div class="metrics">
          <div class="metric-label">Recorded:</div>
          <div class="metric-value">{{startTime}}</div>
          <div class="metric-label">Duration:</div>
          <div class="metric-value">{{duration}} seconds</div>
          <div class="metric-label">Samples:</div>
          <div class="metric-value">{{session.sample_count}}</div>
          <div class="metric-label">CPU time:</div>
          <div class="metric-value">{{cpuTime}} seconds</div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'Header',
  props: ['session'],
  computed: {
    startTime() {
      const date = new Date(this.session.start_time*1000);
      return date.toLocaleString()
    },
    cpuTime() {
      return this.session.cpu_time.toLocaleString(undefined, {maximumSignificantDigits: 3})
    },
    duration() {
      return this.session.duration.toLocaleString(undefined, {maximumSignificantDigits: 3})
    }
  }
}
</script>
<style scoped>
.header {
  background: #292f32;
}
.row {
  display: flex;
  align-items: center;
}
.title {
  font-size: 34px;
  padding-top: 20px;
  padding-bottom: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 10px;
  flex: 1;
}
.metrics {
  display: grid;
  grid-template-columns: auto auto auto auto;
  font-size: 14px;
  text-transform: uppercase;
  grid-gap: 1px 8px;
}

.metric-label {
  font-weight: 600;
  color: #a9abad;
}
.metric-value {
  color: #737779;
  margin-right: 0.5em;
}
</style>
