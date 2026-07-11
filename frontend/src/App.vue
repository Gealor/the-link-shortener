<template>
  <!-- Компонент для динамического рендеринга, какой компонент отрисовать определяет атрибут :is -->
  <component 
    v-for="app in openWindows"
    :is="app.component"
    :key="app.id"
    :window-title="app.windowTitle"
    :window-icon="app.windowIcon"
    :main-icon="app.icon"
    :main-title="app.title"
    :width="app.width"
    :height="app.height"
    :ref="(el) => setWindowRef(app.id, el)" 
    :z-index="getZIndex(app.id)" 
    @close="closeApp(app.id)"
    @focus="bringToFront(app.id)"
  />

  <TaskBar 
    :open-apps="openWindows"
    :quick-launch-apps="quickLaunchApps"
    @launch-app="launchApp"
    @focus-app="focusApp"
  />
</template>

<script setup>
import TaskBar from './components/TaskBar.vue'

import { ref } from 'vue'
import { appsRegistry, quickLaunchApps } from './composables/apps.js'

const openWindows = ref([]) // список открытых окон
const windowRefs = ref({}) // ссылки на компоненты окон, чтобы можно было вызывать их методы
const windowOrder = ref([])  // порядок окон от нижнего к верхнему

function setWindowRef(id, el) {
  if (el) windowRefs.value[id] = el
  else delete windowRefs.value[id]
}

function launchApp(id) {
  const alreadyOpen = openWindows.value.some((w) => w.id === id)
  if (!alreadyOpen) {
    openWindows.value.push(appsRegistry[id])
    windowOrder.value.push(id)
  }
  else focusApp(id)
}

function closeApp(id) {
  openWindows.value = openWindows.value.filter((w) => w.id !== id)
  windowOrder.value = windowOrder.value.filter((w) => w !== id)
}

function focusApp(id) {
  bringToFront(id)
  windowRefs.value[id]?.open?.() // вызывает проброшенный метод open() компонента приложения (TestApp, ExplorerApp)
  // Т.е. цепочка: App.vue вызывает метод open() компонента ExplorerApp/TestApp, который вызывает метод open() компонента ApplicationWindow
}

function bringToFront(id) {
    windowOrder.value = [
        ...windowOrder.value.filter(w => w !== id), // все компоненты с отличающимся id
        id
    ]
}

// z-index - это свойство CSS, которое определяет порядок наложения элементов на странице. 
// Элементы с более высоким z-index будут отображаться поверх элементов с более низким z-index.
function getZIndex(id) {
    const index = windowOrder.value.indexOf(id)
    return 100 + index  // базовый z-index + позиция
}

</script>

<style>
.wrapper {
  width: 100%;
  max-width: 560px;
}

/* Иконка приложения */
.application-icon {
    width: 14px;
    height: 14px;
}

/* Иконка кнопки */
.btn-icon {
    width: 20px;
    height: 20px;
    margin-right: 4px;
}

/* Шапка приложения */
.application-header {
  display: flex;
  align-items: center;
  gap: 2px;
}

/* Разделитель блоков */
.separator {
    display: flex;
    align-items: center; 
    height: 100%;
    margin: 0 0px;
}

.separator.push-right {
    margin-left: auto;
}

.vertical-separator-black {
    width: 1px;
    height: 100%;
    background: #808080;
    box-shadow: 1px 0 0 #fff; /* классический выпуклый разделитель win98 */
    margin: 0 2px;
}

.vertical-separator-white {
    width: 3px;
    height: 80%;
    background: #dddddd;
    box-shadow: 1.5px 1.5px 0 #949494; /* классический выпуклый разделитель win98 */
    border-radius: 0px;
    margin: 0 2px;
}

.little-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0; /* чтобы иконка не сжималась при уменьшении окна */
    margin-right: 5px;
}


.sunken-panel {
    flex: 1;
    min-height: 0;
    background-image: url('@/assets/background-2.jpg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}
</style>
