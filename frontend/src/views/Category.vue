<template>
  <div v-if="category">
    <h1>
      {{ category.name }} <span class="text-muted">#{{ category.id }}</span>
    </h1>
    <hr />
    <div v-if="tasks.length">
      <div class="row row-cols-1 row-cols-md-3">
        <div
          v-for="task in tasks.filter(
            task => task.category !== null && task.category.id === category.id
          )"
          :key="task.id"
          class="tasks"
        >
          <div class="card">
            <div class="card-body">
              <router-link
                :to="{ name: 'Task', params: { id: task.id } }"
                class="btn btn-light"
                ><h2>{{ task.title }}</h2></router-link
              >
              <div v-if="task.category !== null">
                <span class="badge bg-secondary rounded-pill">
                  {{ task.category.name }}</span
                >
              </div>
              <div v-if="task.deadline !== null">
                <hr />
                <p>Due {{ task.deadline | formatDate }}</p>
              </div>
              <hr />
              <div>
                <span>{{ task.spend_minutes }} min spend</span>
              </div>
              <div>
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  v-on:click="addDuration(task)"
                >
                  Add 20min
                </button>
              </div>
              <hr />
              <div>
                <span>Prio: {{ task.virtual_priority.toFixed(2) }}</span
                ><br />
              </div>
            </div>
          </div>
          <br />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "Category",
  props: ["id"],
  async created() {
    try {
      await this.getCategory(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push("/dashboard");
    }
    return this.$store.dispatch("getTasks");
  },
  computed: {
    ...mapGetters({ category: "stateCategory", tasks: "stateTasks" }),
  },
  methods: {
    ...mapActions(["getCategory"]),
  },
};
</script>
