<template>
  <div>
    <label class="input-label">→ вставьте ваш URL</label>
    <div class="input-row">
      <input
        :value="modelValue"
        type="url"
        class="url-input"
        :class="{ 'error-state': error }"
        placeholder="https://example.com/very/long/url..."
        :disabled="loading"
        @input="$emit('update:modelValue', $event.target.value)"
        @keyup.enter="$emit('submit')"
      />
      <button
        class="btn-shorten"
        :class="{ loading }"
        :disabled="loading"
        @click="$emit('submit')"
      >
        {{ loading ? 'загрузка...' : 'сократить' }}
      </button>
    </div>
    <p v-if="error" class="error-msg">
      <span>⚠</span> {{ error }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  error: String,
  loading: Boolean,
})
defineEmits(['update:modelValue', 'submit'])
</script>

<style scoped>
.input-label {
  font-size: 0.78rem;
  font-family: var(--font-mono);
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.75rem;
  display: block;
}

.input-row {
  display: flex;
  gap: 10px;
}

.url-input {
  flex: 1;
  background: var(--surface2);
  border: 1.5px solid var(--border);
  border-radius: 8px;
  padding: 0.85rem 1rem;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--text);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.url-input::placeholder { color: var(--muted); }

.url-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(124, 106, 247, 0.15);
}

.url-input.error-state { border-color: var(--error); }

.btn-shorten {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border: none;
  border-radius: 8px;
  padding: 0.85rem 1.4rem;
  color: #fff;
  font-family: var(--font-display);
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s, transform 0.1s;
  position: relative;
  overflow: hidden;
}

.btn-shorten:hover:not(:disabled) { opacity: 0.9; transform: translateY(-1px); }
.btn-shorten:active:not(:disabled) { transform: translateY(0); }
.btn-shorten:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-shorten.loading::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  animation: shimmer 1s infinite;
}

@keyframes shimmer {
  from { transform: translateX(-100%); }
  to   { transform: translateX(100%); }
}

.error-msg {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--error);
  margin-top: 0.6rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

@media (max-width: 500px) {
  .input-row { flex-direction: column; }
  .btn-shorten { width: 100%; }
}
</style>
