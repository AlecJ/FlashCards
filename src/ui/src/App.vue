<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <div>
    <nav>
      <RouterLink to="/">User</RouterLink>
      <RouterLink to="/admin">Admin</RouterLink>
    </nav>
  </div>

  <RouterView />
</template>

<style>
@import "@/assets/base.css";

body {
  overflow-x: hidden;
  font-family:"minion-pro",times,serif;
  font-size: 1.2em;
}

#app {
  /* max-width: 1280px; */
  margin: 0 auto;
  padding: 2rem;

  font-weight: normal;
}

header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

a {
  text-decoration: none;
  color: var(--blue);
  transition: 0.4s;
}

@media (hover: hover) {
  a:hover {
    background-color: var(--blue-background);
  }
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>
