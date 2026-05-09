<script setup lang="ts">
import DevlogEntry from '../components/DevlogEntry.vue'
</script>

<template>
  <main>
    <h1 style="color: var(--color-heading)">Amethyst Devlog</h1>
    <p>
      So that I don't spam Discord too much. An RSS feed can be found
      <a href="/api/devrss">here</a>.
    </p>
    <DevlogEntry
      v-for="entry in devlog"
      :published="entry.published"
      :title="entry.title"
      :content="entry.content"
    ></DevlogEntry>
  </main>
</template>

<script lang="ts">
import axios from 'axios'

interface DevlogEntry {
  published: string
  title: string
  content: string
}

export default {
  name: 'GetDevlog',
  data(): { devlog: DevlogEntry[] } {
    return {
      devlog: []
    }
  },
  methods: {
    getMessage() {
      axios
        .get('/api/devlog')
        .then((res: { data: DevlogEntry[] }) => {
          this.devlog = res.data
        })
        .catch((error: any) => {
          console.error(error)
        })
    }
  },
  created() {
    this.getMessage()
  }
}
</script>
