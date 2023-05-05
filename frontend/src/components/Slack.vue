<script setup>
</script>

<template>
  <!-- @submit handles any form of submission. -->
  <!-- .prevent keeps the event from bubbling around and doing anything else. -->
  <form @submit.prevent="handleSubmit">
    <label>
      Email:
      <input type="email" v-model="email"/>
    </label>
    <button type="submit">Submit</button>
  </form>
</template>

<script>
export default {
  data() {
    return {
      email: ''
    }
  },
  methods: {
    handleSubmit() {
      // this.$emit('submit', this.email)
      const options = {
      method: 'POST',
      headers: {'Content-Type': 'application/json', 'x-api-key': `${import.meta.env.VITE_SLACK_API_KEY}`},
      body: `{"email":"${this.email}"}`
      };
      fetch(`${import.meta.env.VITE_SLACK_API_ENDPOINT}`, options)
        .then(response => response.json())
        .then(response => console.log(response))
        .catch(err => console.error(err));

    }
  }
}

</script>

<style scoped>

</style>