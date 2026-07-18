<template>
    <ApplicationWindow
        ref="windowRef"
        :title="windowTitle"
        :icon-path="windowIcon"
        :main-icon="mainIcon"
        :height="height"
        :width="width"
        @close="$emit('close')"
    >
        <MyComputerHead :url="windowTitle" :icon="windowIcon" />

        <div class="sunken-panel my-computer">
            <aside class="info-column">
                <div class="info-header">
                    <img :src="selected.icon" :alt="selected.title" class="info-icon" />
                    <h2 class="info-title">{{ selected.title }}</h2>
                    <div class="info-divider"></div>
                </div>
                <p class="info-desc">
                    <template v-for="(part, i) in selected.description" :key="i">
                        <a v-if="typeof part === 'object'" :href="part.href" target="_blank" rel="noopener noreferrer" class="desc-link">{{ part.text }}</a>
                        <template v-else>{{ part }}</template>
                    </template>
                </p>
            </aside>

            <div class="icon-grid">
                <div
                    v-for="item in items"
                    :key="item.id"
                    class="grid-icon"
                    :class="{ selected: selected.id === item.id }"
                    tabindex="0"
                    @click="select(item)"
                    @dblclick="open(item)"
                    @keyup.enter="open(item)"
                >
                    <img :src="item.icon" :alt="item.title" />
                    <span class="grid-label">{{ item.title }}</span>
                </div>
            </div>
        </div>
    </ApplicationWindow>
</template>

<script setup>
import ApplicationWindow from './ApplicationWindow.vue'
import MyComputerHead from './ApplicationHead.vue'

import { ref } from 'vue'

import userIcon from '../assets/icons/msagent-3.png'
import skillsIcon from '../assets/icons/certificate_multiple-1.png'
import projectsIcon from '../assets/icons/briefcase-0.png'
import contactIcon from '../assets/icons/envelope_closed-0.png'
import githubIcon from '../assets/icons/globe_map-0.png'
import resumeIcon from '../assets/icons/notepad_file-0.png'

const props = defineProps({
    windowIcon: String,
    windowTitle: String,
    mainIcon: String,
    width: Number,
    height: Number
})
defineEmits(['close'])

const items = [
    {
        id: 'about',
        title: 'About me',
        icon: userIcon,
        description: 'Python Backend Developer, с 1 годом коммерческого опыта, а также 1 годом разработки pet-проектов. Люблю ретро-интерфейсы, а также в последнее время интересуюсь ИИ-агентами (LangChain/LangGraph).',
    },
    {
        id: 'skills',
        title: 'Skills',
        icon: skillsIcon,
        description: 'Python 3.11+, FastAPI, Docker, Redis, RabbitMQ, Celery, TaskIQ, LangChain, LangGraph, Tensorflow, Vue, JavaScript',
    },
    {
        id: 'github',
        title: 'GitHub',
        icon: githubIcon,
        description: [
            'Открыть мои репозитории на ',
            { text: 'GitHub', href: 'https://github.com/Gealor' },
            '.',
        ],
        action: () => { window.open('https://github.com/Gealor', '_blank') },
    },
    {
        id: 'resume',
        title: 'Resume',
        icon: resumeIcon,
        description: [
            'Открыть резюме на ',
            { text: 'hh.ru', href: 'https://samara.hh.ru/resume/9af95ffdff0d87d6920039ed1f5567316a4e44?hhtmFrom=applicant_profile' },
            '.',
        ],
        action: () => { window.open('https://samara.hh.ru/resume/9af95ffdff0d87d6920039ed1f5567316a4e44?hhtmFrom=applicant_profile', '_blank') },
    },
]

const selected = ref(items[0])

function select(item) {
    selected.value = item
}

function open(item) {
    select(item)
    item.action?.()
}

const windowRef = ref(null)

defineExpose({
    open: () => windowRef.value?.open(),
    close: () => windowRef.value?.close(),
})
</script>

<style scoped>
.my-computer {
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: stretch;
}

.info-column {
    width: 30%;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
    padding: 10px;
    color: #000;
}

.info-header {
    width: 100%;
}

.info-icon {
    width: 48px;
    height: 48px;
    margin-bottom: 8px;
}

.info-title {
    font-size: 24px;
    font-weight: bold;
    line-height: 1.15;
    margin: 0;
}

.info-divider {
    width: 100%;
    height: 1px;
    margin: 8px 0 10px;
    background: linear-gradient(
        to right,
        #ff0000 25%,
        #ffe000 25% 50%,
        #00a000 50% 75%,
        #0000ff 75%
    );
}

.info-desc {
    font-size: 11px;
    line-height: 1.4;
    margin: 0;
}

.icon-grid {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: repeat(auto-fill, 72px);
    grid-auto-rows: 72px;
    gap: 4px;
    padding: 8px;
    align-content: start;
}

.grid-icon {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 4px;
    cursor: pointer;
    font-size: 11px;
    color: #000;
    user-select: none;
}

.grid-icon img {
    width: 32px;
    height: 32px;
}

.grid-icon span {
    display: inline-block;
    padding: 1px 3px;
    text-align: center;
    line-height: 1.2;
    word-break: break-word;
}

/* .grid-icon - класс, который применяется к компоненту, 
.selected - вспомогательный класс, который дополняет стиль при его включении в компонент вместе с .grid-icon, 
span - тег, к которому применяется данный стиль */
.grid-icon.selected span { 
    background-color: #0a246a;
}

.sunken-panel {
    background-image: url('@/assets/background-my-computer.webp');
}
</style>
