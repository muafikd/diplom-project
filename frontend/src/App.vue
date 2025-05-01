<template>
  <SessionNotification />
  <Navbar />
  <router-view />
</template>

<script setup>
import Navbar from "./components/Navbar.vue";
import SessionNotification from './components/SessionNotification.vue';
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  overflow-x: hidden;
}

#app {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>
