<template>
  <div id='app' class="bg">
    <Navbar />
    <Home />
    <router-view></router-view>
  </div>
</template>


<script>
import Home from './views/Home'
import Navbar from './views/Navbar'

export default {
  name:"app",
  components: {
    Home,
    Navbar
  }
}
</script>


<style scoped src="./assets/styles/mystyles.css"></style>

