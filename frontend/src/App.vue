<script setup>
import { RouterView } from 'vue-router'
import Navigation from './components/Navigation.vue';
</script>

<template>
  <Navigation/>
  <suspense>
    <RouterView />
  </suspense>
</template>

<style scoped>

</style>
