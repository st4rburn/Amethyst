<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
    <header>
      <h1 class="purple">Amethyst</h1>
    </header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/challenges">Challenges</RouterLink>
        <RouterLink to="/login">Log In</RouterLink>
      </nav>
    </div>

  <RouterView />
</template>

<style scoped>
header > h1 {
  text-align: center;
  font-size: 72px;
  font-family: "Sixtyfour", system-ui;
}

header {
  padding-top: 24px;
  line-height: 1.5;
  max-height: 120vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 1rem;
  margin-bottom: 1.5rem;
}


nav a {
  color: var(--color-text);
}

nav a.router-link-exact-active {
  color: var(--amethyst-purple);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  font-family: "Exo 2", sans-serif;
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
  font-size: 1rem;
}

nav a:first-of-type {
  border: 0;
}
</style>
