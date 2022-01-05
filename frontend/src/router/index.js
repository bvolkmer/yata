import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";
import Dashboard from "../views/Dashboard.vue";
import Task from "../views/Task.vue"
import EditTask from "../views/EditTask.vue"
import NewTask from "../views/NewTask.vue"
import Category from "../views/Category.vue"

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/new_task",
    name: "New Task",
    component: NewTask,
  },
  {
    path: "/task/:id",
    name: "Task",
    component: Task,
    props: true,
  },
  {
    path: "/task/:id",
    name: "EditTask",
    component: EditTask,
    props: true
  },
  {
    path: "/category/:id",
    name: "Category",
    component: Category,
    props: true
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
