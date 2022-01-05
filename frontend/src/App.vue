<template>
  <div id="app">
    <NavBar />
    <div class="main container">
      <router-view/>
    </div>
  </div>
</template>

<script>

import Vue from 'vue'
import { Datetime } from 'vue-datetime'
import 'vue-datetime/dist/vue-datetime.css'
import moment from 'moment'

Vue.component("datetime", Datetime)
Vue.filter('formatDate', function(value) {
  if (value) {
    var date = moment(String(value))
    //return date.format('DD.MM.YYYY hh:mm')
    return date.calendar()
  }
})

import NavBar from '@/components/NavBar.vue'
export default {
  components: {
    NavBar
  }
}

</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.main {
  padding-top: 5em;
}
</style>
