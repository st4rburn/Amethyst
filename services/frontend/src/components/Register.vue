<script setup lang="ts">
import { ConditionState } from './ConditionsInput.vue';

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
  {
    text: 'Not included in data breaches',
    condition: (data: string, callback: (answer: ConditionState) => void) => {
      const enc = new TextEncoder();
      crypto.subtle.digest("SHA-1", enc.encode(data)).then((hash: ArrayBuffer) => {
        const hex = Array.from(new Uint8Array(hash))
          .map(v => v.toString(16).padStart(2, '0'))
          .join('')
          .toUpperCase(); // The API works in uppercase
        axios.get("https://api.pwnedpasswords.com/range/" + hex.substring(0, 5)).then((res) => {
          const hashes = (res.data as string).split('\r\n'); // The API also works in Windows line endings
          const tail = hex.substring(5);
          for (let potential of hashes) {
            const parts = potential.split(':');
            if (parts[0] === tail) {
              if (parts[1] !== "0") {
                callback(ConditionState.Unfulfilled);
                // Why not
                console.log("Fyi, that password appeared in " + parts[1] + " data breaches.");
                return;
              }
            }
          }
          callback(ConditionState.Fulfilled);
          // Loop through, if the password is there and in a breach, callback with true
        }).catch((e: any) => {
          callback(ConditionState.Error);
          console.log(e);
        })
      }).catch((e: any) => {
        callback(ConditionState.Error);
        console.log(e);
      });
    },
    callback: true,
    deps: [0, 1, 2, 3]
  },
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
