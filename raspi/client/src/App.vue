<template>
  <div id="app">
    <default-navbar></default-navbar>
    <router-view/>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    'default-navbar': Navbar,
  },
};
</script>

<style>
#app {
  margin-top: 20px
}
</style>
