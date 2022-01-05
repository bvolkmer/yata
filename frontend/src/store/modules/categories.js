import axios from "axios"

const state = {
  categories: null,
  category: null
}

const getters = {
  stateCategories: state => state.categories,
  stateCategory: state => state.category
}

const actions = {
  async createCategory({dispatch}, category) {
    await axios.post('categories', category)
    await dispatch('getCategories');
  },
  async getCategories({commit},) {
    let {data} = await axios.get('categories')
    commit('setCategories', data)
  },
  async getCategory({commit}, id) {
    let {data} = await axios.get(`categories/${id}`);
    commit('setCategory', data)
  },
  // eslint-disable-next-line no-empty-pattern
  async updateCategory({}, category) {
    await axios.patch(`categories/${category.id}`, category.form) //TODO: patch vs post
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteNote({}, id) {
    await axios.delete(`categories/${id}`)
  }
}

const mutations = {
  setCategories(state, categories) {
    state.categories = categories
  },
  setCategory(state, category) {
    state.category = category
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
