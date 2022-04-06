import { createRouter, createWebHistory } from "vue-router";
import AdminView from "../views/Admin.vue";
import UserView from "../views/User.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "user",
      component: UserView,
    },
    {
      path: "/admin",
      name: "admin",
      component: AdminView,
    },
  ],
});

export default router;
