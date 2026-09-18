<template>
    <div class="login-backdrop">
        <div class="window login-window">
            <div class="title-bar">
                <div class="title-bar-text">Welcome to Windows</div>
                <div class="title-bar-controls">
                    <button aria-label="Help"></button>
                </div>
            </div>

            <div class="window-body login-shell">
                <menu role="tablist" class="login-tabs">
                    <li
                        v-for="tab in tabs"
                        :key="tab.id"
                        role="tab"
                        :aria-selected="mode === tab.id"
                    >
                        <a href="#" @click.prevent="setMode(tab.id)">{{ tab.label }}</a>
                    </li>
                </menu>

                <div class="window" role="tabpanel">
                    <div class="window-body">
                        <p v-if="authState === AuthState.EXPIRED && mode === 'login'" class="login-expired">
                            Your session has expired. Please log on again.
                        </p>
                        <LoginForm :mode="mode" @change-mode="setMode" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import LoginForm from './LoginForm.vue'
import { AuthState, authState } from '../composables/auth.js'

const tabs = [
    { id: 'login', label: 'Log On' },
    { id: 'register', label: 'Register' },
]

const mode = ref('login')

function setMode(newMode) {
    if (!tabs.some((tab) => tab.id === newMode)) {
        throw new Error(`Invalid mode: ${newMode}`)
    }
    mode.value = newMode
}
</script>

<style scoped>
.login-backdrop {
    position: fixed;
    inset: 0;
    z-index: var(--z-taskbar);
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--bg);
}

.login-window {
    width: 380px;
}

/* Внешний window-body служит только контейнером для вкладок + панели */
.login-shell {
    margin: 8px;
}

.login-tabs {
    padding-left: 6px;
}

.login-expired {
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid #808080;
    font-size: 11px;
    color: #a00000;
}
</style>
