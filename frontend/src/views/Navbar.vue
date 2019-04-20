<template>
  <header id="header" class="alt">
    <a id="logo" href="/"></a>
    <nav>
      <ul>
        <li v-if="this.$route.path == '/'">
          <a href="/map" class="button premium"><span>Go Premium</span></a>
        </li>
      </ul>
    </nav>
  </header>
</template>

<style>
#header {
  width: 100%;
  z-index: 10000;
  top: 0;
  position: fixed;
  line-height: 6em;
  left: 0;
  height: 6em;
  background: #000;
  -moz-transition: background-color 0.2s ease;
  -webkit-transition: background-color 0.2s ease;
  -ms-transition: background-color 0.2s ease;
  transition: background-color 0.2s ease;
}
#header #logo {
  background: url("../assets/images/group_logo.png") center;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: transparent;
  position: fixed;
  width: 9em;
  height: 6em;
  top: 0;
  left: 3em;
}
#header.alt {
  background: transparent;
}
#header.alt #logo {
  opacity: 0;
  pointer-events: none;
}
#header:not(.alt) .button.premium {
  opacity: 0;
  pointer-events: none;
}
#header .button {
  cursor: pointer;
}
#header nav {
  height: inherit;
  line-height: inherit;
  position: absolute;
  right: 0;
  top: 0;
}
#header nav > ul {
  list-style: none;
  margin: 0;
  padding: 0;
  white-space: nowrap;
}
#header nav > ul > li {
  display: inline-block;
  padding: 0;
}
#header nav > ul > li > a {
  border: 0;
  color: #fff;
  display: block;
  font-size: 0.8em;
  letter-spacing: 0.225em;
  padding: 0 1.5em;
  text-transform: uppercase;
}
@media screen and (max-width: 736px) {
  #header nav > ul > li > a {
    padding: 0 0 0 1.5em;
  }
}
#header nav > ul > li:first-child {
  margin-left: 0;
}
#header .premium span {
  background-color: rgb(255, 153, 0);
  color: #000;
  font-weight: 700;
  padding: 1em;
  border-radius: 6px;
}
#header a.premium {
  text-decoration: none;
}
#header a.premium:hover {
  opacity: .9;
}
#header a.premium:active {
  opacity: .7;
}
</style>

<script>
export default {
  name: "Navbar",
  mounted() {
    console.debug("| Header Mounted")
    this.handleNavbar()
  },
  methods: {
    handleNavbar () {
      const $header = document.getElementById('header')
      window.onscroll = () => {
        if(document.body.scrollTop==0&&document.documentElement.scrollTop==0) {
          $header.classList.add('alt')
        } else {
          $header.classList.remove('alt')
        }
      }
    }
  }
};
</script>
