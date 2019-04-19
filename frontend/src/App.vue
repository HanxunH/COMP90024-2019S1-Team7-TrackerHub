<template>
  <div id='app' class="bg">
    <router-view></router-view>
      <div class="div"></div>
    <button class="button" onclick="window.location.href='/map'" v-if="this.$route.path == '/'">Go Premium</button>
  </div>
</template>

<style scoped src="./assets/styles/mystyles.css"></style>

