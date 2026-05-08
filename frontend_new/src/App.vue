<template>
  <GlowOrb position="top-left" />
  <GlowOrb position="bottom-right" />

  <div class="wrapper">
    <AppHeader />

    <div class="card">
      <div class="card-inner">
        <transition name="fade" mode="out-in">

          <UrlInput
            v-if="!result"
            key="input"
            v-model="url"
            :error="error"
            :loading="loading"
            @submit="shortenUrl"
          />

          <UrlResult
            v-else
            key="result"
            :result="result"
            :copied-key="copied"
            @copy="copy"
            @reset="reset"
          />

        </transition>
      </div>
    </div>

    <AppFeatures />
    <AppToast :message="toast" />
  </div>
</template>

<script setup>
import GlowOrb     from './components/GlowOrb.vue'
import AppHeader   from './components/AppHeader.vue'
import UrlInput    from './components/UrlInput.vue'
import UrlResult   from './components/UrlResult.vue'
import AppFeatures from './components/AppFeatures.vue'
import AppToast    from './components/AppToast.vue'

import { useShortener } from './composables/useShortener.js'
import { useClipboard } from './composables/useClipboard.js'

const { url, result, error, loading, shortenUrl, reset } = useShortener()
const { copied, toast, copy } = useClipboard()
</script>

<style scoped>
.wrapper {
  width: 100%;
  max-width: 560px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 2rem;
  margin-bottom: 1rem;
}

.card-inner {
  position: relative;
  min-height: 120px;
}
</style>
