<template>
  <div>
    <section>
      <h1>Current Task</h1>
      <hr />
      <div v-if="tasks.length" class="container">
        <div class="row justify-content-center">
          <div class="col">
            <router-link
              :to="{ name: 'Task', params: { id: tasks[0].id } }"
              class="btn btn-light card-title"
              ><h2>{{ tasks[0].title }}</h2></router-link
            >
          </div>
        </div>
        <div
          class="row justify-content-md-center"
          v-if="tasks[0].category !== null"
        >
          <div class="col">
            <span class="badge bg-secondary rounded-pill">
              <router-link
                :to="{
                  name: 'Category',
                  params: { id: tasks[0].category.id },
                }"
                class="text-light"
                style="text-decoration: none"
              >
                {{ tasks[0].category.name }}</router-link
              ></span
            >
          </div>
        </div>
        <hr />
        <div
          v-if="tasks[0].deadline !== null"
          v-bind:class="
            isTomorrow(tasks[0])
              ? 'bg-warning'
              : isEarlierThanTomorrow(tasks[0])
              ? 'bg-danger'
              : ''
          "
        >
          <p><strong>Deadline:</strong> {{ tasks[0].deadline | formatDate }}</p>
        </div>
        <div class="row">
          <div class="col">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Score</h5>
                <p class="card-text">
                  {{ tasks[0].virtual_priority.toFixed(2) }}
                </p>
              </div>
            </div>
          </div>
          <div class="col">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Priority</h5>
                <p class="card-text">{{ tasks[0].priority }}</p>
              </div>
            </div>
          </div>
          <div class="col">
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">Time spend</h5>
                <div class="card-text">
                  <span>{{ tasks[0].spend_minutes }} min</span>
                </div>
              </div>
              <div class="card-footer">
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
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Ping",
  created: function () {
    return this.$store.dispatch("getTasks");
  },
  computed: {
    ...mapGetters({ tasks: "stateTasks" }),
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
        const now = new Date();
        const tomorrow = new Date(
          now.getFullYear(),
          now.getMonth(),
          now.getDate() + 1
        );
        const deadline = new Date(task.deadline);
        if (tomorrow.getTime() > deadline.getTime()) {
          return true;
        }
      }
      return false;
    },
    isTomorrow(task) {
      if (task.deadline !== null) {
        const now = new Date();
        const tomorrow = new Date(
          now.getFullYear(),
          now.getMonth(),
          now.getDate() + 1
        );
        const deadline = new Date(task.deadline);
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
