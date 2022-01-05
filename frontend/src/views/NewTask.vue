
<template>
  <div>
    <section>
      <h1>Add new task</h1>
      <hr />
      <br />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="title" class="form-label">Title:</label>
          <input
            type="text"
            name="title"
            v-model="form.title"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="text" class="form-label">Text:</label>
          <textarea
            name="text"
            v-model="form.text"
            class="form-control"
          ></textarea>
        </div>
        <div class="mb-3">
          <label for="priority" class="form-label">Priority:</label>
          <input
            type="number"
            name="priority"
            v-model="form.priority"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="spend_minutes" class="form-label">Spend Minutes:</label>
          <input
            type="number"
            name="spend_minutes"
            v-model="form.spend_minutes"
            class="form-control"
          />
        </div>
        <div class="mb-3">
          <label for="deadline" class="form-label">Deadline:</label>
          <datetime v-model="form.deadline" type="datetime"></datetime>
          <!--input
            type="datetime"
            name="deadline"
            v-model="form.deadline"
            class="form-control"
          /-->
        </div>
        <label for="category" class="form-label">Category:</label>
        <select class="form-select" name="category" v-model="form.category">
          <option value="null" selected></option>
          <option v-for="category in categories" v-bind:key="category.id" v-bind:value="category.id">
            {{category.name}}</option>
        </select>
        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </section>
  </div>
</template>

<script>

import { mapActions, mapGetters } from "vuex";
export default {
  name: "NewTask",
  data() {
    return {
      form: {
        title: "",
        text: "",
        priority: 10,
        spend_minutes: 0,
        deadline: null,
        category: null
      },
    };
  },
  created: function () {
    return this.$store.dispatch("getCategories");
  },
  computed: {
    ...mapGetters({ categories: "stateCategories" }),
  },
  methods: {
    ...mapActions(["updateTask"]),
    async submit() {
      try {
        let task = {
          id: null,
          form: this.form,
        };
        if (task.form.category === "") {
          task.form.category = null;
        }
        if (task.form.deadline === "") {
          task.form.deadline = null;
        }
        await this.updateTask(task);
        this.$router.push({ name: "Dashboard" });
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>
