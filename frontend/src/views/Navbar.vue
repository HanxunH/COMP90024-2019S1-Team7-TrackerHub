<template>
    <div id ="navbar" v-if="this.$route.path == '/map'">
      <nav class=" navbar navbar-light bg-gray float-right">
        <b-button-group>
          <b-button onclick="window.location.href='/'">Home</b-button>
          <b-dropdown right text="Menu-1">
            <b-dropdown-item>Item 1</b-dropdown-item>
            <b-dropdown-item>Item 2</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>Item 3</b-dropdown-item>
          </b-dropdown>
          <b-dropdown right text="Menu-2">
            <b-dropdown-item>Item 1</b-dropdown-item>
            <b-dropdown-item>Item 2</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item>Item 3</b-dropdown-item>
          </b-dropdown>
        </b-button-group>
      </nav>
    </div>
</template>


<script>
    export default {
        name: "Navbar"
    }
</script>
