<template>
  <main>
    <Chat />
  </main>
</template>

<script setup>
// Yeni oluşturduğumuz Chat bileşenini import ediyoruz
import Chat from './components/ChatComponent.vue';
</script>

<style>
/* Tüm sayfayı kaplayan ve varsayılan boşlukları kaldıran
  global stilleri buraya koymak daha doğrudur.
*/
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f4f7f9;
}

main {
  width: 100%;
  height: 100vh;
}
</style>
