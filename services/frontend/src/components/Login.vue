<script lang="ts">
import axios from 'axios';

export default {
  name: 'LoginForm',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    submit(e: Event): void {
      // API call to log in, what data do we return?
      // Navigate to challenges if successful
      alert("Test alert for now.");
      axios.get('/api/login')
        .then((res: { data: string; }) => {
          this.msg = res.data;
        })
        .catch((error: any) => {
          console.error(error);
        });
      e.preventDefault();
    }
  }
};
</script>


<template>
  <form method="POST" @submit="submit">
    <label for="username">Username/Email</label><input id="username" name="username" required type="text">
    <br>
    <br>
    <label for="password">Password</label><input id="password" name="password" required type="password">
    <br>
    <br>
    <br>
    <input name="submit" type="submit" value="Login">
  </form>
</template>

<style scoped>

h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}
</style>
