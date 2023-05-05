<script setup>
const email = "getemail@from.somewhere"
const options = {
  method: 'POST',
  headers: {'Content-Type': 'application/json', 'x-api-key': `${import.meta.env.VITE_SLACK_API_KEY}`},
  body: `{"email":"${email}"}`
};

fetch(`${import.meta.env.VITE_SLACK_API_ENDPOINT}`, options)
  .then(response => response.json())
  .then(response => console.log(response))
  .catch(err => console.error(err));
</script>

<template>

</template>

<style scoped>

</style>