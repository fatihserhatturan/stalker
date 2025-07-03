<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
</script>

<style>


body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f4f7f9;
}

#app {
  width: 100%;
  height: 100vh;
}

.router-enter-active,
.router-leave-active {
  transition: all 0.3s ease;
}

.router-enter-from,
.router-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
