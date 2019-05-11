<template>
  <div id="home" v-if="this.$route.path == '/'">
    <!-- Introduction -->
    <section id="banner">
      <div class="inner">
        <div class="logo"></div>
        <p>
          COMP90024 - Cluster and Cloud Computing <br>
          Assignment Two
        </p>
      </div>
      <a href="#intro" class="more">Learn More</a>    
    </section>
    <section id="intro" class="wrapper center">
      <div class="inner">
        <h2>Group Member</h2>
        <p>Hanxun Huang - 975781</p>
        <p>Haonan Chen - 930614</p>
        <p>Lihuan Zhang - 945003</p>
        <p>Xu Wang - 979895</p>
        <p>Xu Yang - 961717</p>
        <p class="button premium" onclick="window.location.href='/map'">
          <a>Go Premium</a>
        </p>
      </div>
    </section>
  </div>
</template>


<script>
export default {
  name: "Home"
};
</script>


<style src="./../assets/styles/mystyles.css"></style>