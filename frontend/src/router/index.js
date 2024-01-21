import { createWebHistory, createRouter } from "vue-router";
import System from "../views/System.vue";
import RoomSearch from "../views/RoomSearch.vue";
import RoomInfo from "../views/RoomInfo.vue";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import('preline')


const routes = [
  {
    path: "/system",
    name: "System",
    component: System,
    children:[
      {
        path: "",
        name: "RoomSearch",
        component: RoomSearch,
      }, 
      {
        path: "roominfo/:roomName",
        name: "RoomInfo",
        component: RoomInfo,
        props: true 
      },     
    ]
  },
  {
    path: "/",
    name: "home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;