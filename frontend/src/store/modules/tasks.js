import axios from "axios";

const state = {
  tasks: null,
  task: null,
};

const getters = {
  stateTasks: (state) => state.tasks,
  stateTask: (state) => state.task,
};

const actions = {
  async createTask({ dispatch }, task) {
    await axios.post("tasks", task);
    await dispatch("getTasks");
  },
  async getTasks({ commit }) {
    let { data } = await axios.get("tasks");
    commit("setTasks", data);
  },
  async getTask({ commit }, id) {
    let { data } = await axios.get(`tasks/${id}`);
    commit("setTask", data);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateTask({dispatch}, task) {
    task.form.id = task.id;
    await axios.post(`tasks/`, task.form); //TODO: patch vs post
    await dispatch("getTasks")
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteTask({dispatch}, id) {
    await axios.delete(`tasks/${id}`);
    await dispatch("getTasks")
  },
};

const mutations = {
  setTasks(state, tasks) {
    state.tasks = tasks.sort((a, b) =>
      a.virtual_priority > b.virtual_priority
        ? -1
        : b.virtual_priority > a.virtual_priority
        ? 1
        : 0
    );
  },
  setTask(state, task) {
    state.task = task;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
