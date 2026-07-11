<template>
  <div class="field-row-stacked">
    <label for="url-field">Вставьте ваш URL</label>
    <div class="input-row">
      <input
        id="url-field"
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
        :disabled="loading"
        @click="$emit('submit')"
      >
        {{ loading ? 'Загрузка...' : 'Сократить' }}
      </button>
    </div>

    <p v-if="error" class="error-msg">
      <img :src="warningIcon" alt="Warning" class="error-icon">
      {{ error }}
    </p>
  </div>
</template>

<script setup>
import warningIcon from '../assets/icons/msg_warning-2.png'

defineProps({
  modelValue: String,
  error: String,
  loading: Boolean,
})
defineEmits(['update:modelValue', 'submit'])
</script>

<style scoped>
.input-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.url-input {
  flex: 1;
}

.url-input.error-state {
  outline: 1px solid #ff0000;
  outline-offset: -1px;
}

.btn-shorten {
  white-space: nowrap;
  min-width: 90px;
}

.btn-shorten:disabled {
  cursor: not-allowed;
}

.error-msg {
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px; 
}

.error-icon {
  width: 16px;
  height: 16px;
}

@media (max-width: 500px) {
  .input-row { flex-direction: column; align-items: stretch; }
  .btn-shorten { width: 100%; }
}
</style>
