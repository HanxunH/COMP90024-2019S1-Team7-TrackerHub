<template>
  <header id="header" class="alt">
    <a id="logo" href="/"></a>
    <nav id="nav"></nav>
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

/*
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

#header nav > ul > li > a.menuToggle {
  outline: 0;
  position: relative;
}

#header nav > ul > li > a.menuToggle:after {
  background-image: url("../assets/images/bars.svg");
  background-position: right center;
  background-repeat: no-repeat;
  content: "";
  display: inline-block;
  height: 3.75em;
  vertical-align: top;
  width: 2em;
}

@media screen and (max-width: 736px) {
  #header nav > ul > li > a.menuToggle {
    padding: 0 1.5em;
  }
  #header nav > ul > li > a.menuToggle span {
    display: none;
  }
}

@media screen and (max-width: 736px) {
  #header nav > ul > li > a {
    padding: 0 0 0 1.5em;
  }
}

#header nav > ul > li:first-child {
  margin-left: 0;
}

#header.alt {
  background: transparent;
}

#header.alt h1 {
  pointer-events: none;
  opacity: 0;
} */
</style>


<script>
export default {
  name: "Navbar",
  mounted() {
    console.debug("| Header Mounted");
    this.initHeader();
  },
  methods: {
    initHeader() {
    }
  }
};
</script>
