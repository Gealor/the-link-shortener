<template>
    <div 
        v-if="isOpen"
        ref="windowEl"
        class="window" 
        :class="{ minimized: isMinimized }"
        :style="windowStyle"
        @mousedown="$emit('focus')"
    >
        <div class="title-bar" @mousedown="startDrag">
            <div class="title-bar-text application-header">
                <img :src="props.iconPath" alt="icon" class="application-icon">
                {{ props.title}}
            </div>
            <div class="title-bar-controls">
                <button aria-label="Minimize" @click="toggleMinimize"></button>
                <button aria-label="Maximize" @click="toggleMaximize"></button>
                <button aria-label="Close" @click="close"></button>
            </div>
        </div>
        <div class="window-body">
            <slot /> <!-- Сюда будет вставлен контент окна. Все что будет помещено между ApplicationWindow будет помещено на место <slot /> -->
        </div>
        <div class="status-bar">
            <p class="status-bar-field" style="width: 50%;"></p>
            <p class="status-bar-field"></p>
            <p class="status-bar-field" style="display: flex; align-items: center; user-select: none;">
                <img :src="mainIcon" alt="" class="little-icon">
                <span>{{ mainTitle }}</span>
            </p>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

import missingIcon from '../assets/icons/msagent-3.png'

const props = defineProps({
    title: {
        type: String,
        default: 'Application Window'
    },
    mainTitle: {
        type: String
    },
    iconPath: {
        type: String,
        default: missingIcon,
    },
    mainIcon: {
        type: String,
        default: missingIcon,
    },
    width: {
        type: Number,
        default: 400,
    },
    height: Number,
    zIndex: {
        type: Number,
        default: 100,
    }
});
const emit = defineEmits(['close', 'focus'])

// Переменная для ссылки на элемент окна
const windowEl = ref(null);

// Позиция окна
const defaultPos = ref({ x: 100, y: 100 })
const pos = ref({ x: 100, y: 100 });

// Переменные для перетаскивания окна
const dragOffset = ref({ x: 0, y: 0 });
const isDragging = ref(false);

// Состояние окна
const isOpen = ref(true)
const isMinimized = ref(false)
const isMaximized = ref(false)

const windowStyle = computed(() => {
    if (isMaximized.value) {
        return { 
            left: '0px',
            top: '0px',
            position: 'fixed',
            width: '100vw',
            height: 'calc(100vh - var(--taskbar-height) + 2px)',
            zIndex: props.zIndex, // z-index - это свойство CSS, которое определяет порядок наложения элементов на странице. 
            // Элементы с более высоким z-index будут отображаться поверх элементов с более низким z-index.
        }
    }

    const style = {
        left: pos.value.x + 'px',
        top: pos.value.y + 'px',
        position: 'fixed',
        width: props.width + 'px',
        zIndex: props.zIndex, // z-index - это свойство CSS, которое определяет порядок наложения элементов на странице. 
        // Элементы с более высоким z-index будут отображаться поверх элементов с более низким z-index.
    }

    if (!isMinimized.value && props.height) {
        style.height = props.height + 'px'
    }

    return style;
})

function toggleMinimize() {
    isMaximized.value = false
    isMinimized.value = !isMinimized.value
}

function toggleMaximize() {
    isMaximized.value = !isMaximized.value
    if (isMaximized.value) isMinimized.value = false
}

function close() {
    pos.value = { x: defaultPos.value.x, y: defaultPos.value.y }    
    isMinimized.value = false
    isMaximized.value = false
    isOpen.value = false
    emit('close')
}

function startDrag(event) {
    if (isMaximized.value) return
    isDragging.value = true
    dragOffset.value = {
        x: event.clientX - pos.value.x,
        y: event.clientY - pos.value.y,
    }
    window.addEventListener('mousemove', onDrag)
    window.addEventListener('mouseup', stopDrag)
}

function onDrag(event) {
    if (!isDragging.value) return
    pos.value = {
        x: event.clientX - dragOffset.value.x,
        y: event.clientY - dragOffset.value.y,
    }
}

function stopDrag() {
    isDragging.value = false
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
}

function open() {
    isOpen.value = true;
    isMinimized.value = false;
}

defineExpose({ open, close }) // Чтобы родительский компонент мог управлять окном через ref

onMounted(() => {
    const rect = windowEl.value.getBoundingClientRect()
    pos.value = {
        x: (window.innerWidth - rect.width) / 2,
        y: (window.innerHeight - rect.height) / 2,
    }
});

onUnmounted(() => {
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
});

</script>

<style scoped>
.title-bar {
    user-select: none;
}

.window.minimized .window-body { display: none; }

.window.minimized .status-bar { display: none; }

.window {
    display: flex;
    flex-direction: column;
}

.window-body {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
}
</style>