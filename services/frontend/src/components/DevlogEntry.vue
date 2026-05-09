<script setup lang="ts">
defineProps<{
  published: string
  title: string
  content: string
}>()

function formatTime(published: string): string {
  // Z sets the timezone to UTC
  const date = new Date(published + 'Z')
  const year = date.getFullYear().toString()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  return year + '-' + month + '-' + day
}
</script>

<template>
  <article class="devlog-entry">
    <h2>{{ title }}</h2>
    <time v-bind:datetime="formatTime(published)">{{ formatTime(published) }}</time>
    <div class="devlog-content" v-html="content"></div>
  </article>
</template>

<style scoped>
article {
  margin-top: 24px;
  padding: 14px;
  background-color: var(--color-background-mute);
  border: solid 2px var(--color-border);
}
h2 {
  font-family: var(--minor-heading-font);
  color: var(--color-inner-heading);
  margin-bottom: -8px;
}
time {
  font-size: 0.9em;
  color: var(--color-inner-text);
}
div.devlog-content {
  margin-top: 8px;
  color: var(--color-inner-text);
}
</style>
