import Vue from 'vue';
import Router from 'vue-router';
import Devices from '../components/Devices.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/devices',
      name: 'Devices',
      component: Devices,
    },
  ],
});
