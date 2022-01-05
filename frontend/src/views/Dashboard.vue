<template>
  <div>
    <section>
      <h1>Tasks</h1>
      <router-link to="/new_task" class="btn btn-primary">New Task</router-link>
      <hr />
      <br />

      <div v-if="tasks.length">
        <div class="row row-cols-1 row-cols-md-3">
          <div v-for="task in tasks" :key="task.id" class="tasks">
            <div
              class="card mb-4"
              v-bind:class="isTomorrow(task) ? 'bg-warning' : ((isEarlierThanTomorrow(task))?'bg-danger':'')"
            >
              <router-link
                :to="{ name: 'Task', params: { id: task.id } }"
                class="btn btn-light card-header"
                ><h2>{{ task.title }}</h2></router-link
              >
              <div class="card-body">
                <span
                  v-if="task.category !== null"
                  class="badge bg-secondary rounded-pill mb-3"
                >
                  <router-link
                    :to="{
                      name: 'Category',
                      params: { id: task.category.id },
                    }"
                    class="text-light"
                    style="text-decoration: none"
                  >
                    {{ task.category.name }}</router-link
                  ></span
                >
                <div v-if="task.deadline !== null">
                  <p>Due {{ task.deadline | formatDate }}</p>
                  <hr />
                </div>
                <div class="row justify-content-center">
                  <div class="col-7 align-self-center">
                    <span>{{ task.spend_minutes }} min spend</span>
                  </div>
                  <div class="col-5">
                    <button
                      type="button"
                      class="btn btn-primary btn-sm"
                      v-on:click="addDuration(task)"
                    >
                      Add 20min
                    </button>
                  </div>
                </div>
              </div>
              <div class="card-footer">
                <span>Score: {{ task.virtual_priority.toFixed(2) }}</span
                ><br />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else>
        <p>Nothing to see.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Dashboard",
  created: function () {
    this.$store.dispatch("getCategories");
    this.$store.dispatch("getTasks");
  },
  computed: {
    ...mapGetters({ tasks: "stateTasks", categories: "stateCategories" }),
  },
  methods: {
    ...mapActions(["updateTask", "getTask"]),
    async addDuration(task) {
      try {
        task = {
          id: task.id,
          form: task,
        };
        task.form.spend_minutes += 20;
        await this.updateTask(task);
        //this.$router.push({ name: "Task", params: { id: task.id } });
      } catch (error) {
        console.log(error);
      }
    },
    isEarlierThanTomorrow(task) {
      if (task.deadline !== null) {
        const now = new Date()
        const tomorrow = new Date(
          now.getFullYear(),
          now.getMonth(),
          now.getDate() + 1
        );
        const deadline = new Date(task.deadline)
          if (tomorrow.getTime() > deadline.getTime() ) {
          return true;
        }
      }
      return false;
    },
    isTomorrow(task) {
      if (task.deadline !== null) {
        const now = new Date()
        const tomorrow = new Date(
          now.getFullYear(),
          now.getMonth(),
          now.getDate() + 1
        );
        const deadline = new Date(task.deadline)
        if (
          tomorrow.getFullYear() == deadline.getFullYear() &&
          tomorrow.getMonth() == deadline.getMonth() &&
          tomorrow.getDate() == deadline.getDate()
        ) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>
