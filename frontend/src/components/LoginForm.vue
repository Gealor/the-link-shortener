<template>
    <div class="login-body">
        <img :src="keyIcon" alt="" class="login-icon">

        <div class="login-main">
            <p class="login-hint">{{ hint }}</p>

            <div class="field-row login-field">
                <label for="login-username" class="login-label">
                    <span class="mnemonic">U</span>ser&nbsp;name:
                </label>
                <input
                    id="login-username"
                    v-model="username"
                    type="text"
                    autocomplete="username"
                    :disabled="loading"
                    @keyup.enter="focusPassword"
                >
            </div>

            <div class="field-row login-field">
                <label for="login-password" class="login-label">
                    <span class="mnemonic">P</span>assword:
                </label>
                <input
                    id="login-password"
                    ref="passwordField"
                    v-model="password"
                    type="password"
                    :autocomplete="isRegister ? 'new-password' : 'current-password'"
                    :disabled="loading"
                    @keyup.enter="isRegister ? focusRepeat() : submit()"
                >
            </div>

            <div v-if="isRegister" class="field-row login-field">
                <label for="login-repeat-password" class="login-label">
                    <span class="mnemonic">C</span>onfirm&nbsp;password:
                </label>
                <input
                    id="login-repeat-password"
                    ref="repeatField"
                    v-model="repeatPassword"
                    type="password"
                    autocomplete="new-password"
                    :disabled="loading"
                    @keyup.enter="submit"
                >
            </div>
        </div>

        <div class="login-buttons">
            <button class="default" :disabled="loading" @click="submit">
                {{ loading ? 'Please wait…' : 'OK' }}
            </button>
            <button :disabled="loading" @click="cancel">Cancel</button>
        </div>
    </div>

    <p v-if="error" class="login-status login-status--error">
        <img :src="warningIcon" alt="Warning" class="login-status-icon">
        {{ error }}
    </p>
    <p v-else-if="notice" class="login-status">
        {{ notice }}
    </p>
</template>

<script setup>
import { computed, nextTick, ref} from 'vue'
import keyIcon from '../assets/icons/key_padlock-0.png'
import warningIcon from '../assets/icons/msg_warning-2.png'
import { login, register } from '../composables/auth.js'

const props = defineProps({
    mode: { type: String, default: 'login' },
})

const emit = defineEmits(['changeMode'])

const isRegister = computed(() => props.mode === 'register')
const hint = computed(() =>
    isRegister.value
        ? 'Choose a user name and password to create a new account.'
        : 'Type a user name and password to log on to Windows.'
)

const username = ref('')
const password = ref('')
const repeatPassword = ref('')
const error = ref('')
const notice = ref('')
const loading = ref(false)

const passwordField = ref(null)
const repeatField = ref(null)

function focusPassword() {
    passwordField.value?.focus()
}

function focusRepeat() {
    repeatField.value?.focus()
}

// Клиентские минимумы — зеркалят ограничения бэкенда (мгновенный фидбек, экономия запроса)
const MIN_NICKNAME = 2
const MIN_PASSWORD = 8

// OK и Enter выбирают обработчик по текущему режиму
function submit() {
    return isRegister.value ? submitRegister() : submitLogin()
}

async function submitLogin() {
    if (loading.value) return
    error.value = ''
    notice.value = ''

    if (!username.value.trim()) {
        error.value = 'Enter a user name.'
        return
    }

    loading.value = true
    try {
        await login(username.value, password.value)
    } catch (e) {
        error.value = e.message || 'Could not log on.'
    } finally {
        loading.value = false
    }
}

async function submitRegister() {
    if (loading.value) return
    error.value = ''
    notice.value = ''

    if (username.value.trim().length < MIN_NICKNAME) {
        error.value = `The user name must be at least ${MIN_NICKNAME} characters.`
        return
    }
    if (password.value.length < MIN_PASSWORD) {
        error.value = `The password must be at least ${MIN_PASSWORD} characters.`
        return
    }
    if (password.value !== repeatPassword.value) {
        error.value = 'The passwords do not match.'
        return
    }

    loading.value = true
    try {
        await register(username.value, password.value, repeatPassword.value)
        // бэкенд не логинит — переводим на вход, логин/пароль оставляем для входа в один клик
        repeatPassword.value = ''
        emit('changeMode', 'login')
        await nextTick()
        notice.value = 'Account created. You can now log on.'
    } catch (e) {
        error.value = e.message || 'Could not create the account.'
    } finally {
        loading.value = false
    }
}

function cancel() {
    username.value = ''
    password.value = ''
    repeatPassword.value = ''
    error.value = ''
    notice.value = ''
}
</script>

<style scoped>
.login-body {
    display: flex;
    align-items: flex-start;
    gap: 12px;
}

.login-icon {
    flex-shrink: 0;
    width: 32px;
    height: 32px;
    margin-top: 2px;
}

.login-main {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.login-hint {
    font-size: 11px;
    line-height: 1.35;
}

.login-field {
    margin: 0;
    gap: 6px;
}

.login-label {
    width: 78px;
    flex-shrink: 0;
    justify-content: flex-end;
    text-align: right;
}

.login-field input {
    flex: 1;
    min-width: 0;
}

.login-buttons {
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 6px;
    width: 75px;
}

.login-status {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 10px 2px 2px;
    font-size: 11px;
}

.login-status--error {
    color: #a00000;
}

.login-status-icon {
    width: 16px;
    height: 16px;
    flex-shrink: 0;
}
</style>
