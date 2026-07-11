<template>
  <fieldset class="result">
    <legend class="result-legend">
      <img :src="checkIcon" alt="" class="result-icon" />
      Ссылка сокращена
    </legend>

    <div class="field-row-stacked">
      <label>Исходный URL</label>
      <div class="input-row">
        <input class="field-input" :value="result.full_url" readonly />
        <button
          class="btn-copy"
          :class="{ copied: copiedKey === 'original' }"
          @click="$emit('copy', result.full_url, 'original')"
        >
          {{ copiedKey === 'original' ? 'Скопировано' : 'Копировать' }}
        </button>
      </div>
    </div>

    <div class="field-row-stacked">
      <label>Сокращённая ссылка</label>
      <div class="input-row">
        <input class="field-input highlight" :value="result.full_slug" readonly />
        <button
          class="btn-copy"
          :class="{ copied: copiedKey === 'short' }"
          @click="$emit('copy', result.full_slug, 'short')"
        >
          {{ copiedKey === 'short' ? 'Скопировано' : 'Копировать' }}
        </button>
      </div>
    </div>

    <div class="field-row-stacked">
      <label>Код</label>
      <div class="sunken-panel slug-box">{{ result.slug }}</div>
    </div>

    <hr />

    <button class="btn-reset" @click="$emit('reset')">
      ↩ Сократить ещё одну ссылку
    </button>
  </fieldset>
</template>

<script setup>
import checkIcon from '../assets/icons/check-0.png'

defineProps({
  result: Object,
  copiedKey: String,
})
defineEmits(['copy', 'reset'])
</script>

<style scoped>
.result {
  margin: 0;
  padding: 10px 12px 12px;
  background-color: rgba(0, 0, 0, 0.25)
}

.result-legend {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 4px;
}

.result-icon {
  width: 14px;
  height: 14px;
}

.field-row-stacked {
  margin-bottom: 10px;
}

.input-row {
  display: flex;
  gap: 8px;
}

.field-input {
  flex: 1;
}

.field-input.highlight {
  font-weight: bold;
}

.btn-copy {
  cursor: pointer;
  white-space: nowrap;
  min-width: 96px;
}

.btn-copy.copied {
  color: #006400;
}

.slug-box {
  padding: 8px;
  text-align: center;
  font-size: 1rem;
  font-weight: bold;
  letter-spacing: 0.08em;
  margin: 0;
}

hr {
  margin: 10px 0;
}

.btn-reset {
  width: 100%;
  padding: 6px;
  cursor: pointer;
}
</style>
