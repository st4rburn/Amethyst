<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Check if a string contains a character in chars
function contains_one_of(text: string, chars: string): boolean {
  for (let char of chars) {
    if (text.includes(char)) {
      return true;
    }
  }
  return false;
}
// Check if a string contains a character not in chars
function contains_more_than(text: string, chars: string): boolean {
  for (let char of text) {
    if (!chars.includes(char)) {
      return true;
    }
  }
  return false;
}
const lowercase = "abcdefghijklmnopqrstuvwxyz";
const uppercase = lowercase.toUpperCase();
const digits = "1234567890";
const alphanumeric = lowercase + uppercase + digits;

const username_conditions = [
  { text: 'Between 3 and 32 characters', condition: (data: string) => {
    return 3 <= data.length && data.length <= 32;
  }},
];
const password_conditions = [
  { text: 'At least 12 characters', condition: (data: string) => {
    return data.length >= 12;
  }},
  { text: 'Contains both uppercase and lowercase letters', condition: (data: string) => {
    return contains_one_of(data, lowercase) && contains_one_of(data, uppercase);
  }},
  { text: 'Contains at least one number', condition: (data: string) => {
    return contains_one_of(data, digits);
  }},
  { text: 'Contains at least one symbol (!@#$%, etc.)', condition: (data: string) => {
    return contains_more_than(data, alphanumeric);
  }},
];
const confirm_conditions = [
  { text: 'Matches password', condition: (data: string) => {
    return (document.getElementById("password-field") as HTMLFormElement).value === data;
  }},
];
</script>

<script lang="ts">
import axios from 'axios';
import ConditionsInput from './ConditionsInput.vue';

export default {
  name: 'RegisterForm',
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
      axios.get('/api/register')
        .then((res: { data: string; }) => {
          this.msg = res.data;
        })
        .catch((error: any) => {
          console.error(error);
        });
      e.preventDefault();
    },

  },
};
</script>


<template>
  <form method="POST" @submit="submit">
    <ConditionsInput name="username" type="text" label="Username" :conditions="username_conditions" desc="(will be visible)"/>
    <br>
    <br>
    <label for="email">Email <i>(shared with no one)</i></label><input id="email" name="email" required type="email">
    <br>
    <br>
    <ConditionsInput name="password" type="password" label="Password" :conditions="password_conditions"/>
    <br>
    <br>
    <ConditionsInput name="confirm" type="password" label="Confirm Password" :conditions="confirm_conditions"/>
    <br>
    <br>
    <br>
    <input name="submit" type="submit" value="Register">
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
