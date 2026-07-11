<template>
    <ApplicationWindow
        ref="windowRef"
        :title="windowTitle"
        :icon-path="windowIcon"
        :main-icon="mainIcon"
        :width="width"
        :height="height"
        @close="$emit('close')"
    >
        <InternetExplorerHead url="https://Shortify/" :icon="windowIcon" />

        <div class="sunken-panel">
            <UrlInput
                v-if="!result"
                key="input"
                v-model="url"
                :error="error"
                :loading="loading"
                @submit="shortenUrl"    
            />

            <UrlResult
                v-else
                key="result"
                :result="result"
                :copied-key="copied"
                @copy="copy"
                @reset="reset"
            />
        </div>
        
    </ApplicationWindow>
</template>

<script setup>
import UrlInput    from './UrlInput.vue'
import UrlResult   from './UrlResult.vue'
import ApplicationWindow from './ApplicationWindow.vue'
import InternetExplorerHead from './ApplicationHead.vue'

import { useShortener } from '../composables/useShortener.js'
import { useClipboard } from '../composables/useClipboard.js'

import { ref } from 'vue'

const { url, result, error, loading, shortenUrl, reset } = useShortener()
const { copied, copy } = useClipboard()

defineEmits(['close'])

const props = defineProps({
    windowIcon: String,
    windowTitle: String,
    mainIcon: String,
    width: Number,
    height: Number
})

const windowRef = ref(null) // ссылка на компонент ApplicationWindow
defineExpose({ // пробрасываемые методы, чтобы родительский компонент (App.vue) мог вызывать их
    open: () => windowRef.value?.open(), // пробрасываемый метод open(), который вызывает проброшенный метод open() компонента ApplicationWindow, чтобы можно было открывать окно приложения из родительского компонента (App.vue)
    close: () => windowRef.value?.close(),
})

</script>

<style scoped>
.title-bar {
    user-select: none;
}

.sunken-panel {
    padding: 10px;
}
</style>