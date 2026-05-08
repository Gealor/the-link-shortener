<template>
  <div>
    <div class="result-header">
      <span class="result-badge">✓ готово</span>
      <span class="result-title">Ссылка сокращена</span>
    </div>

    <div class="field-group">
      <span class="field-label">исходный URL</span>
      <div class="field-row">
        <input class="field-input" :value="result.full_url" readonly />
        <button
          class="btn-copy"
          :class="{ copied: copiedKey === 'original' }"
          @click="$emit('copy', result.full_url, 'original')"
        >
          {{ copiedKey === 'original' ? '✓ скопировано' : 'копировать' }}
        </button>
      </div>
    </div>

    <div class="field-group">
      <span class="field-label">сокращённая ссылка</span>
      <div class="field-row">
        <input class="field-input highlight" :value="result.full_slug" readonly />
        <button
          class="btn-copy"
          :class="{ copied: copiedKey === 'short' }"
          @click="$emit('copy', result.full_slug, 'short')"
        >
          {{ copiedKey === 'short' ? '✓ скопировано' : 'копировать' }}
        </button>
      </div>
    </div>

    <div class="field-group">
      <span class="field-label">код</span>
      <div class="slug-box">{{ result.slug }}</div>
    </div>

    <hr class="divider" />

    <button class="btn-reset" @click="$emit('reset')">
      ↩ сократить ещё одну ссылку
    </button>
  </div>
</template>

<script setup>
defineProps({
  result: Object,
  copiedKey: String,
})
defineEmits(['copy', 'reset'])
</script>

<style scoped>
.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 1.5rem;
}

.result-badge {
  background: rgba(62, 255, 163, 0.1);
  border: 1px solid rgba(62, 255, 163, 0.3);
  color: var(--success);
  font-family: var(--font-mono);
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 20px;
}

.result-title {
  font-size: 1rem;
  font-weight: 600;
}

.field-group { margin-bottom: 1.2rem; }

.field-label {
  font-size: 0.72rem;
  font-family: var(--font-mono);
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.5rem;
  display: block;
}

.field-row {
  display: flex;
  gap: 8px;
}

.field-input {
  flex: 1;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.7rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--muted);
  outline: none;
}

.field-input.highlight {
  border-color: var(--accent);
  color: var(--accent);
  background: rgba(124, 106, 247, 0.06);
}

.btn-copy {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.7rem 1rem;
  color: var(--muted);
  font-family: var(--font-mono);
  font-size: 0.78rem;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-copy:hover { border-color: var(--accent); color: var(--accent); }

.btn-copy.copied {
  border-color: var(--success);
  color: var(--success);
  background: rgba(62, 255, 163, 0.06);
}

.slug-box {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 500;
  color: var(--accent2);
  letter-spacing: 0.1em;
}

.divider {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.5rem 0;
}

.btn-reset {
  width: 100%;
  background: transparent;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem;
  color: var(--muted);
  font-family: var(--font-display);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover { border-color: var(--text); color: var(--text); }
</style>
