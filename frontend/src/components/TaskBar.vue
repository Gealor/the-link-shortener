<template>
    <div class="taskbar">
        <div ref="startMenuWrapper">
            <StartMenu :visible="startMenuOpen" @select="onMenuSelect" />
        </div>

        <button
            ref="startButtonRef"
            class="start-button"
            :class="{ 'button-active': startMenuOpen }"
            @click="startMenuOpen = !startMenuOpen"
        >
            <img :src="startIcon" alt="Start" class="btn-icon">
            <span class="start-btn-text">Start</span>
        </button>

        <div class="separator">
            <div class="vertical-separator-black"></div>
            <div class="vertical-separator-white"></div>
        </div>

        <!-- Быстрый запуск -->
        <div class="quick-launch">
            <img 
                v-for="app in quickLaunchApps"
                :key="app.id"
                :src="app.icon"
                :alt="app.title"
                class="btn-icon"
                @click="$emit('launch-app', app.id)"
            >
        </div>

        <div class="separator">
            <div class="vertical-separator-black"></div>
            <div class="vertical-separator-white"></div>
        </div>

        <!-- Открытые приложения -->
        <button
            v-for="app in openApps"
            :key="app.id"
            class="default task-button button-active"
            @click="$emit('focus-app', app.id)"
            @contextmenu.prevent="openTaskContextMenu($event, app.id)"
        >
            <img :src="app.icon" :alt="app.title" class="btn-icon">
            <span class="btn-text">{{ app.title }}</span>
        </button>

        <div ref="taskContextMenuWrapper">
            <TaskContextMenu
                :visible="taskContextMenu.visible"
                :x="taskContextMenu.x"
                :y="taskContextMenu.y"
                @close="handleCloseApp"
            />
        </div>

        <div class="separator push-right">
            <div class="vertical-separator-black"></div>
        </div>

        <!-- Группа уведомлений -->
        <div class="field-border-disabled notification-area">
            <div class="notification-icons">
                <img :src="mouseIcon" alt="Mouse" class="notification-area-icon">
                <img :src="loudspeakerIcon" alt="Loudspeaker" class="notification-area-icon">
                <img :src="networkIcon" alt="Network" class="notification-area-icon">
            </div>
            <span class="btn-text">{{ currentTime }}</span> 
        </div>
    </div>
</template>

<script setup>
import startIcon from '../assets/icons/windows-5.png'
import mouseIcon from '../assets/icons/mouse-3.png'
import loudspeakerIcon from '../assets/icons/loudspeaker_rays-1.png'
import networkIcon from '../assets/icons/network_normal_two_pcs-1.png'
import StartMenu from './StartMenu.vue'
import TaskContextMenu from './TaskContextMenu.vue'

import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
    openApps: {
        type: Array,
        default: () => [],
    },
    quickLaunchApps: {
        type: Array,
        default: () => [],
    }
})
const emit = defineEmits(['launch-app', 'focus-app', 'close-app'])


// Стартовое меню
const startMenuOpen = ref(false)
const startMenuWrapper = ref(null)
const startButtonRef = ref(null)

function onMenuSelect() {
    // Пока пункты меню захардкожены и без реального действия — просто закрываем меню
    startMenuOpen.value = false
}

function onDocumentClick(event) {
    if (startMenuOpen.value) {
        const insideMenu = startMenuWrapper.value?.contains(event.target)
        const onButton = startButtonRef.value?.contains(event.target)
        if (!insideMenu && !onButton) startMenuOpen.value = false
    }

    if (taskContextMenu.value.visible && !taskContextMenuWrapper.value?.contains(event.target)) {
        closeTaskContextMenu()
    }
}

// Контекстное меню открытого приложения (ПКМ по кнопке в панели задач)
const taskContextMenu = ref({ visible: false, x: 0, y: 0, appId: null })
const taskContextMenuWrapper = ref(null)

function openTaskContextMenu(event, appId) {
    taskContextMenu.value = { visible: true, x: event.clientX, y: window.innerHeight - event.clientY, appId }
}

function closeTaskContextMenu() {
    taskContextMenu.value.visible = false
}

function handleCloseApp() {
    if (taskContextMenu.value.appId) emit('close-app', taskContextMenu.value.appId)
    closeTaskContextMenu()
}

// Время
const currentTime = ref('')

function updateTime() {
    const now = new Date()
    let hours = now.getHours()
    const minutes = now.getMinutes().toString().padStart(2, '0')
    const ampm = hours >= 12 ? 'PM' : 'AM'
    hours = hours % 12 || 12
    currentTime.value = `${String(hours).padStart(2, '0')}:${minutes} ${ampm}`
}
let intervalId

onMounted(() => {
    updateTime()
    intervalId = setInterval(updateTime, 1000)
    document.addEventListener('mousedown', onDocumentClick)
})

onUnmounted(() => {
    clearInterval(intervalId)
    document.removeEventListener('mousedown', onDocumentClick)
})
</script>

<style scoped>
/* Панель задач */
.taskbar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: var(--taskbar-height);
    z-index: var(--z-taskbar); /* панель задач всегда должна быть выше окон приложений */
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 2px 4px;
    box-sizing: border-box;
    background: silver; /* стандартный win98-фон */
    border-top: 1px solid #fff;
}

/* Быстрый запуск */
.quick-launch {
    display: flex;
    align-items: center;
    margin-right: 20px;
}

.quick-launch .btn-icon {
    box-sizing: content-box; /* чтобы padding не сжимал саму картинку*/
    padding: 4px;
    margin: 0px; /* компенсируем padding, чтобы соседние иконки не раздвигались */
    cursor: pointer;
}

.quick-launch .btn-icon:hover {
    box-shadow: inset 1px 1px #fff, inset -1px -1px #808080; /* приподнятый бортик, как у остальных win98-элементов */
}

/* Кнопка задачи */
.task-button {
    display: flex;
    align-items: center;
    margin: 0;
    padding-left: 3px;
    min-width: 50px;
    max-width: 200px;
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-family: var(--font-family-title);
    font-size: var(--font-size-title);
    padding: 2px 6px;
    height: 30px;
}

/* Стартовая кнопка */
.start-button {
    width: 80px;
    display: flex;
    gap: 2px;
    align-items: center;
    justify-content: center;
    height: 30px;
}

.button-active {
    box-shadow: inset -1px -1px #ffffff, inset 1px 1px #0a0a0a, inset -2px -2px #dfdfdf, inset 2px 2px #808080;
}


/* Текст кнопок */
.start-btn-text {
    font-size: 14px;
    font-weight: bold;
}

.btn-text {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 13px;
    min-width: 0;   
    font-family: var(--font-family-default);
}

/* Область уведомлений */
.notification-area {
    display: flex;
    align-items: center;
    gap: 2px;
    height: 30px;
    width: 150px;
    padding: 4px;
}

.notification-area .btn-text {
    margin-left: auto;
    margin-right: 8px;
    user-select: none;
}

.notification-icons {
    display: flex;
    align-items: center;
    gap: 2px;
    margin-left: auto;
    margin-right: auto;
}

.notification-area-icon {
    width: 18px;
    height: 18px;
    margin-right: 4px;
}
</style>