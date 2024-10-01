<script setup lang="ts">
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
</script>

<template>
    <div :class="{hidden: registering}">
        <Login/>
        <br>
        <a @click="register">Register instead!</a>
    </div>
    <div :class="{hidden: !registering}">
        <Register/>
        <br>
        <a @click="login">Back to login</a>
    </div>
</template>

<script lang="ts">
export default {
  name: 'LoginView',
  data() {
    return {
      registering: false
    };
  },
  methods: {
    login(e: Event) {
        this.registering = false;
        e.preventDefault();
    },
    register(e: Event) {
        this.registering = true;
        e.preventDefault();
    }
  }
};
</script>

<style>
div.hidden {
    display: none;
}

input {
    padding: 12px 20px;
    width: 100%;
    background-color: var(--color-background-mute);
    border: solid 2px var(--color-border);
    color: var(--color-input);
}
input[type=submit] {
    background-color: var(--color-background-primary-button);
    border: solid 2px var(--color-background-primary-button-border);
    color: var(--color-heading);
}

label i {
    font-size: 0.8em;
}
</style>
