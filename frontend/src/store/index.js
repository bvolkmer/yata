import createPersistedState from "vuex-persistedstate";
import Vue from 'vue'
import Vuex from 'vuex'

import tasks from "./modules/tasks"
import categories from "./modules/categories"

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    tasks,
    categories,
  },
  plugins: [createPersistedState()]
})
