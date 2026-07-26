<template>
    <div class="desktop" @click.self="selectedId = null">
        <div
            v-for="app in apps"
            :key="app.id"
            class="desktop-icon"
            :class="{ selected: selectedId === app.id }"
            tabindex="0"
            @click="select(app.id)"
            @dblclick="open(app.id)"
            @keyup.enter="open(app.id)"
        >
            <img :src="app.icon" :alt="app.title" class="icon-image" />
            <span class="icon-label">{{ app.title }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
    apps: {
        type: Array,
        default: () => [],
    },
})
const emit = defineEmits(['launch-app'])

const selectedId = ref(null)

function select(id) {
    selectedId.value = id
}

function open(id) {
    select(id)
    emit('launch-app', id)
}
</script>

<style scoped>
.desktop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: var(--taskbar-height);
    z-index: var(--z-desktop, 1);
    display: grid;
    grid-auto-flow: column;
    grid-template-rows: repeat(auto-fill, 75px);
    grid-auto-columns: 75px;
    gap: 4px;
    padding: 8px;
    justify-content: start;
}

.desktop-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 4px;
    cursor: pointer;
    user-select: none;
}

.icon-image {
    width: 32px;
    height: 32px;
}

.icon-label {
    font-size: 12px;
    font-family: var(--font-family-default);
    color: #fff;
    text-align: center;
    line-height: 1.2;
    word-break: break-word;
    padding: 1px 3px;
}

.desktop-icon.selected .icon-label {
    background-color: var(--color-highlight);
    text-shadow: none;
    outline: 1px dotted #fff;
    outline-offset: -1px;
}

.desktop-icon.selected .icon-image {
    filter: brightness(0.8) sepia(1) hue-rotate(180deg) saturate(3);
}
</style>
