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

        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--right"
            @mousedown="startResize(ResizeDirection.RIGHT, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--left"
            @mousedown="startResize(ResizeDirection.LEFT, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--bottom"
            @mousedown="startResize(ResizeDirection.BOTTOM, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--top"
            @mousedown="startResize(ResizeDirection.TOP, $event)"
        ></div>

        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--corner resize-handle--top-left"
            @mousedown="startResize(ResizeDirection.TOP_LEFT, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--corner resize-handle--top-right"
            @mousedown="startResize(ResizeDirection.TOP_RIGHT, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--corner resize-handle--bottom-left"
            @mousedown="startResize(ResizeDirection.BOTTOM_LEFT, $event)"
        ></div>
        <div
            v-if="!isMaximized && !isMinimized"
            class="resize-handle resize-handle--corner resize-handle--bottom-right"
            @mousedown="startResize(ResizeDirection.BOTTOM_RIGHT, $event)"
        ></div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

import missingIcon from '../assets/icons/msagent-3.png'

// Базовый минимальный размер окна (без учёта шапки) - само окно (title-bar + status-bar + чуть контента)
const MIN_WIDTH_DEFAULT = 200
const MIN_HEIGHT_DEFAULT = 120

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
    minWidth: {
        type: Number,
        default: null,
    },
    minHeight: {
        type: Number,
        default: null,
    },
    zIndex: {
        type: Number,
        default: () => Number(getComputedStyle(document.documentElement).getPropertyValue('--z-windows-base')) || 100,
    }
});
const emit = defineEmits(['closeWindow', 'focus'])

// Переменная для ссылки на элемент окна
const windowEl = ref(null);

// Позиция окна
const defaultPos = ref({ x: 100, y: 100 })
const pos = ref({ x: 100, y: 100 });

// Переменные для перетаскивания окна
const dragOffset = ref({ x: 0, y: 0 });
const isDragging = ref(false);

// Размер окна
const size = ref({ width: props.width, height: props.height ?? null })

// Измеренные (по реальному DOM) размеры шапки - суммарная высота и максимальная
// требуемая ширина среди всех .bar-header строк, которые сейчас реально отрисованы в слоте
// (панели, отключённые через v-if, просто не будут рассматриваться)
const measuredHeaderWidth = ref(0)
const measuredHeaderHeight = ref(0)

const effectiveMinWidth = computed(() =>
    props.minWidth ?? Math.max(MIN_WIDTH_DEFAULT, measuredHeaderWidth.value)
)
const effectiveMinHeight = computed(() =>
    props.minHeight ?? (MIN_HEIGHT_DEFAULT + measuredHeaderHeight.value)
)

function measureHeader() {
    if (!windowEl.value) return
    const rows = windowEl.value.querySelectorAll('.window-body .bar-header')

    let totalHeight = 0
    let maxWidth = 0

    rows.forEach((row) => {
        // высота задаётся явно в CSS (.bar-header--menu/actions/search), поэтому просто читаем её
        totalHeight += row.getBoundingClientRect().height

        // ширина строки сейчас "растянута" под текущую ширину окна (width: calc(100% + 16px)),
        // поэтому чтобы узнать реально необходимую ширину контента — на мгновение снимаем
        // ограничение и тут же возвращаем обратно (без промежуточной отрисовки кадра)
        const prevWidth = row.style.width
        row.style.width = 'max-content'
        maxWidth = Math.max(maxWidth, row.scrollWidth)
        row.style.width = prevWidth
    })

    measuredHeaderHeight.value = totalHeight
    measuredHeaderWidth.value = maxWidth
}

// Переменные для ресайза окна
const ResizeDirection = Object.freeze({
    RIGHT: 'right',
    LEFT: 'left',
    BOTTOM: 'bottom',
    TOP: 'top',
    TOP_LEFT: 'top-left',
    TOP_RIGHT: 'top-right',
    BOTTOM_LEFT: 'bottom-left',
    BOTTOM_RIGHT: 'bottom-right',
})
const isResizing = ref(false)
const resizeDirection = ref(null) // одно из значений ResizeDirection
const resizeStart = ref({ x: 0, y: 0, width: 0, height: 0, posX: 0, posY: 0 })

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
        width: size.value.width + 'px',
        zIndex: props.zIndex, // z-index - это свойство CSS, которое определяет порядок наложения элементов на странице.
        // Элементы с более высоким z-index будут отображаться поверх элементов с более низким z-index.
    }

    if (!isMinimized.value && size.value.height) {
        style.height = size.value.height + 'px'
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
    size.value = { width: props.width, height: props.height ?? null }
    isMinimized.value = false
    isMaximized.value = false
    isOpen.value = false
    emit('closeWindow')
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

function startResize(direction, event) {
    if (isMaximized.value) return
    event.preventDefault() // чтобы перенос не выделял текст на странице
    isResizing.value = true
    resizeDirection.value = direction
    resizeStart.value = {
        x: event.clientX,
        y: event.clientY,
        width: size.value.width,
        height: size.value.height ?? windowEl.value.getBoundingClientRect().height,
        posX: pos.value.x,
        posY: pos.value.y,
    }
    window.addEventListener('mousemove', onResize)
    window.addEventListener('mouseup', stopResize)
}


// Обработчики стороны
function resizeRight(event) {
    const delta = event.clientX - resizeStart.value.x
    size.value.width = Math.max(effectiveMinWidth.value, resizeStart.value.width + delta);
}

function resizeLeft(event) {
    // Растягиваем влево: правый край должен остаться на месте,
    // поэтому позицию (x) сдвигаем ровно на столько, на сколько реально изменилась ширина
    const delta = event.clientX - resizeStart.value.x
    const newWidth = Math.max(effectiveMinWidth.value, resizeStart.value.width - delta)
    pos.value.x = resizeStart.value.posX + (resizeStart.value.width - newWidth)
    size.value.width = newWidth
}

function resizeBottom(event) {
    const delta = event.clientY - resizeStart.value.y
    size.value.height = Math.max(effectiveMinHeight.value, resizeStart.value.height + delta)
}

function resizeTop(event) {
    // Растягиваем вверх: нижний край должен остаться на месте
    const delta = event.clientY - resizeStart.value.y
    const newHeight = Math.max(effectiveMinHeight.value, resizeStart.value.height - delta)
    pos.value.y = resizeStart.value.posY + (resizeStart.value.height - newHeight)
    size.value.height = newHeight
}

// Диагональные обработчики - просто комбинируют по одному горизонтальному и одному вертикальному
function resizeTopLeft(event) {
    resizeLeft(event)
    resizeTop(event)
}

function resizeTopRight(event) {
    resizeRight(event)
    resizeTop(event)
}

function resizeBottomLeft(event) {
    resizeLeft(event)
    resizeBottom(event)
}

function resizeBottomRight(event) {
    resizeRight(event)
    resizeBottom(event)
}

// Регистр, который ставит в соответствие одной стороне некоторый обработчик
const mapDirectionToHandle = {
    [ResizeDirection.RIGHT]: resizeRight,
    [ResizeDirection.LEFT]: resizeLeft,
    [ResizeDirection.BOTTOM]: resizeBottom,
    [ResizeDirection.TOP]: resizeTop,
    [ResizeDirection.TOP_LEFT]: resizeTopLeft,
    [ResizeDirection.TOP_RIGHT]: resizeTopRight,
    [ResizeDirection.BOTTOM_LEFT]: resizeBottomLeft,
    [ResizeDirection.BOTTOM_RIGHT]: resizeBottomRight,
}

function onResize(event) {
    if (!isResizing.value) return

    const handler = mapDirectionToHandle[resizeDirection.value]
    if (!handler) {
        console.warn("Не найден обработчик для направления")
        return
    }

    handler(event)
}

function stopResize() {
    isResizing.value = false
    resizeDirection.value = null
    window.removeEventListener('mousemove', onResize)
    window.removeEventListener('mouseup', stopResize)
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
    measureHeader()
});

onUnmounted(() => {
    window.removeEventListener('mousemove', onDrag)
    window.removeEventListener('mouseup', stopDrag)
    window.removeEventListener('mousemove', onResize)
    window.removeEventListener('mouseup', stopResize)
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
    margin: 0; /* у 98.css по умолчанию margin: 8px — обнуляем, чтобы шапка/контент шли встык к краям окна */
    display: flex;
    flex-direction: column;
}

.resize-handle {
    position: absolute;
}

.resize-handle--right {
    top: 0;
    right: -3px;
    width: 6px;
    height: 100%;
    cursor: ew-resize;
}

.resize-handle--bottom {
    left: 0;
    bottom: -3px;
    width: 100%;
    height: 6px;
    cursor: ns-resize;
}

.resize-handle--left {
    top: 0;
    left: -3px;
    width: 6px;
    height: 100%;
    cursor: ew-resize;
}

.resize-handle--top {
    left: 0;
    top: -3px;
    width: 100%;
    height: 6px;
    cursor: ns-resize;
}

.resize-handle--corner {
    width: 8px;
    height: 8px;
}

.resize-handle--top-left {
    top: -3px;
    left: -3px;
    cursor: nwse-resize;
}

.resize-handle--top-right {
    top: -3px;
    right: -3px;
    cursor: nesw-resize;
}

.resize-handle--bottom-left {
    bottom: -3px;
    left: -3px;
    cursor: nesw-resize;
}

.resize-handle--bottom-right {
    bottom: -3px;
    right: -3px;
    cursor: nwse-resize;
}
</style>