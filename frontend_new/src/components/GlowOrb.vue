<template>
  <div class="glow-orb" :class="`glow-orb--${position}`"></div>
</template>

<script setup>
defineProps({
  position: {
    type: String,
    default: 'top-left', // 'top-left' | 'bottom-right'
  }
})
</script>

<style scoped>
.glow-orb {
  position: fixed;
  pointer-events: none;
  border-radius: 50%;
  z-index: 0;
}

.glow-orb--top-left {
  top: -20%;
  left: -10%;
  width: 50vw;
  height: 50vw;
  background: radial-gradient(circle, rgba(124, 106, 247, 0.12) 0%, transparent 70%);
}

.glow-orb--bottom-right {
  bottom: -10%;
  right: -10%;
  width: 40vw;
  height: 40vw;
  background: radial-gradient(circle, rgba(224, 95, 255, 0.08) 0%, transparent 70%);
}
</style>
