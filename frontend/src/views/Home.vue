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
      <a href="#intro" class="more scrolly">Learn More</a>    
    </section>
    <section id="intro" class="wrapper center">
      <div class="inner">
        <h2>Group Member</h2>
        <p>Hanxun Huang - 000000</p>
        <p>Haonan Chen - 000000</p>
        <p>Lihuan Zhang - 000000</p>
        <p>Xu Wang - 979895</p>
        <p>Xu Y - 000000</p>
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