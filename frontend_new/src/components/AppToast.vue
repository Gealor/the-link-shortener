<template>
  <transition name="toast">
    <div v-if="message" class="toast">{{ message }}</div>
  </transition>
</template>

<script setup>
defineProps({
  message: String,
})
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--surface2);
  border: 1px solid var(--success);
  color: var(--success);
  font-family: var(--font-mono);
  font-size: 0.82rem;
  padding: 0.7rem 1.4rem;
  border-radius: 30px;
  z-index: 999;
  pointer-events: none;
  white-space: nowrap;
}
</style>
