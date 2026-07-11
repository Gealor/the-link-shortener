<template>
    <div class="taskbar">
        <button class="start-button">
            <img :src="startIcon" alt="Start" class="btn-icon">
            <span class="start-btn-text">Start</span>
        </button>

        <div class="separator">
            <div class="vertical-separator-black"></div>
            <div class="vertical-separator-white"></div>
        </div>

        <div class="quick-launch" style="margin-right: 20px">
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

        <button 
            v-for="app in openApps"
            :key="app.id"
            class="default task-button"
            @click="$emit('focus-app', app.id)"
        >
            <img :src="app.icon" :alt="app.title" class="btn-icon">
            <span class="btn-text">{{ app.title }}</span>
        </button>

        <div class="separator push-right">
            <div class="vertical-separator-black"></div>
        </div>

        <div class="field-border-disabled notification-area" style="padding: 4px">
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
defineEmits(['launch-app', 'focus-app'])


// Время
const currentTime = ref('')

function updateTime() {
    const now = new Date()
    let hours = now.getHours()
    const minutes = now.getMinutes().toString().padStart(2, '0')
    const ampm = hours >= 12 ? 'PM' : 'AM'
    hours = hours % 12 || 12
    currentTime.value = `${hours}:${minutes} ${ampm}`
}
let intervalId

onMounted(() => {
    updateTime()
    intervalId = setInterval(updateTime, 1000)
})

onUnmounted(() => {
    clearInterval(intervalId)
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
    gap: 2px;
}

/* Кнопка задачи */
.task-button {
    width: 80px;
    display: flex;
    min-width: 0;
    align-items: center;
    padding: 2px 6px;
    white-space: nowrap; /* чтобы текст не переносился при сжатии */
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
}

/* Область уведомлений */
.notification-area {
    display: flex;
    align-items: center;
    gap: 2px;
    height: 30px;
    width: 150px;
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