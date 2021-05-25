<template>
    <b-navbar variant=dark type=dark>
        <b-navbar-brand>{{this.$route.meta.title}}</b-navbar-brand>
        <b-navbar-nav>
            <b-nav-item :to="{name: 'Devices'}">Home</b-nav-item>
        </b-navbar-nav>
    </b-navbar>
</template>

<script>
export default {

};
</script>

<style>

</style>
