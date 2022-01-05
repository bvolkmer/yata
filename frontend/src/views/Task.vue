<template>
  <div v-if="task" class="container">
    <div class="row justify-content-end">
      <div class="col-1">
        <router-link
          :to="{ name: 'EditTask', params: { id: task.id } }"
          class="btn btn-primary"
          >Edit</router-link
        >
      </div>
      <div class="col-1">
        <button @click="removeTask()" class="btn btn-danger">Delete</button>
      </div>
    </div>
    <div class="row justify-content-md-center">
      <div class="col">
        <h1>
          {{ task.title }} <span class="text-muted">#{{ task.id }}</span>
        </h1>
      </div>
    </div>
    <div class="row justify-content-md-center" v-if="task.category !== null">
      <div class="col">
        <span class="badge bg-secondary rounded-pill">
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
      </div>
    </div>
    <hr />
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Score</h5>
            <p class="card-text">{{ task.virtual_priority.toFixed(2) }}</p>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Priority</h5>
            <p class="card-text">{{ task.priority }}</p>
          </div>
        </div>
      </div>
      <div class="col">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">Time spend</h5>
            <p class="card-text">{{ task.spend_minutes }} minutes</p>
          </div>
        </div>
      </div>
      <div v-if="task.deadline !== null">
        <p><strong>Deadline:</strong> {{ task.deadline | formatDate }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Task",
  props: ["id"],
  async created() {
    try {
      await this.getTask(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push("/dashboard");
    }
  },
  computed: {
    ...mapGetters({ task: "stateTask" }),
  },
  methods: {
    ...mapActions(["getTask", "deleteTask"]),
    async removeTask() {
      try {
        await this.deleteTask(this.id);
        this.$router.push("/dashboard");
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
