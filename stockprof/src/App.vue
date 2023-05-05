<template>
  <div id="wrapper">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <router-link class="navbar-item is-dark" to="/">Home</router-link>
          <!-- <router-link class="navbar-item is-dark" to="/about">About</router-link> -->
        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link  to="/profile"  v-if="isAuthenticated" class="button is-primary">
              <strong>Personal Profile</strong>
            </router-link >
            <router-link  to="/signup" v-else class="button is-primary">
                <strong>Sign Up</strong>
            </router-link>
            <a  v-if="isAuthenticated" @click="logout" class="button is-danger">
              Logout
            </a>
            <router-link  v-else to="/login" class="button is-light">
                Log in
            </router-link>
          </div>
        </div>
      </div>
    </nav>
    <section class="section">
      <router-view />
    </section>

  </div>
</template>

<style lang="scss">
@import '../node_modules/bulma';

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>

<script>
import { mapGetters } from 'vuex'
import axios from 'axios'
export default {
  computed: {
    ...mapGetters(['isAuthenticated'])
  },
  methods :{
    logout() {
      axios.defaults.headers.common["Authorization"] = ""
      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userid")
      this.$store.commit('removeToken')
      this.$router.push('/')
    },
  }
}
</script>