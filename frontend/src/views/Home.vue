<template>
  <div id='home' v-if="this.$route.path == '/'">
      <div class="div"></div>
    <button class="button" onclick="window.location.href='/map'">Go Premium</button>
  </div>
</template>


<script>
    export default {
        name: "Home"
    }
</script>


<style scoped src="./../assets/styles/mystyles.css"></style>