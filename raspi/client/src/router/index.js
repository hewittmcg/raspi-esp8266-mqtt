import Vue from 'vue';
import Router from 'vue-router';
import Devices from '../components/Devices.vue';
import Data from '../components/Data.vue';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      redirect: '/devices',
    },
    {
      path: '/devices',
      name: 'Devices',
      component: Devices,
      meta: { title: 'Device List' },
    },
    {
      path: '/device/:id',
      name: 'Data',
      component: Data,
      meta: { title: 'Device Data' },
    },
  ],
});

// Handle page titles
const DEFAULT_TITLE = 'Raspberry Pi Server';
router.afterEach((to) => {
  Vue.nextTick(() => {
    document.title = to.meta.title ? to.meta.title : DEFAULT_TITLE;
  });
});

export default router;
