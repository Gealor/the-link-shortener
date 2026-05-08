<template>
  <div class="features">
    <div v-for="feature in features" :key="feature.title" class="feature">
      <div class="feature-icon">{{ feature.icon }}</div>
      <div class="feature-title">{{ feature.title }}</div>
      <div class="feature-desc">{{ feature.desc }}</div>
    </div>
  </div>
</template>

<script setup>
const features = [
  { icon: '⚡', title: 'Быстро',   desc: 'мгновенный результат' },
  { icon: '🔒', title: 'Безопасно', desc: 'данные защищены'      },
  { icon: '📱', title: 'Везде',     desc: 'любое устройство'     },
]
</script>

<style scoped>
.features {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.feature {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1rem;
  text-align: center;
}

.feature-icon { font-size: 1.4rem; margin-bottom: 0.5rem; }

.feature-title {
  font-size: 0.82rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.feature-desc {
  font-size: 0.72rem;
  color: var(--muted);
  font-family: var(--font-mono);
}

@media (max-width: 500px) {
  .features { grid-template-columns: 1fr; }
}
</style>
