<template>
  <header class="header">
    <div class="logo">
      <div class="logo-icon">🔗</div>
      <span class="logo-text">shortify</span>
    </div>
    <p class="subtitle">// сокращайте ссылки мгновенно</p>
  </header>
</template>

<style scoped>
.header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.75rem;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.logo-text {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  color: var(--muted);
  font-size: 0.9rem;
  font-family: var(--font-mono);
  letter-spacing: 0.02em;
}
</style>
