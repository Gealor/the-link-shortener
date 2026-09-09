import { ref } from 'vue'

import { ApiError, apiFetch } from './api.js'

// Одно состояние авторизации на всё приложение:
//   CHECKING      - идёт первая проверка сессии, экраны не показываем
//   ANONYMOUS     - сессии нет (первый визит / после выхода)
//   AUTHENTICATED - сессия есть, currentUser заполнен
//   EXPIRED       - сессию оборвал сервер во время работы (экран логина покажет пояснение)
export const AuthState = Object.freeze({
    CHECKING: 'checking',
    ANONYMOUS: 'anonymous',
    AUTHENTICATED: 'authenticated',
    EXPIRED: 'expired',
})

export const authState = ref(AuthState.CHECKING)

// Данные текущего пользователя { id, nickname, is_active } | null.
// Источник правды - HttpOnly-кука на бэкенде, здесь только её отражение из GET /auth/me.
export const currentUser = ref(null)


// Спросить бэкенд, кто мы. Нужно на старте приложения / после перезагрузки страницы,
// когда токен сессии есть в куке, а состояния в памяти ещё нет.
// 401 - сессии нет; сетевой сбой на старте трактуем так же (просто покажем логин).
export async function fetchSession() {
    try {
        currentUser.value = await apiFetch('/auth/me')
        authState.value = AuthState.AUTHENTICATED
    } catch (e) {
        currentUser.value = null
        authState.value = AuthState.ANONYMOUS
        if (!(e instanceof ApiError)) throw e
    }
}


// Вход. При успехе бэкенд ставит HttpOnly-куку session_id и возвращает самого пользователя —
// отдельный запрос к /auth/me не нужен.
// Бросает ApiError (401 - неверные данные, 403 - заблокирован, 0 - сервер недоступен).
export async function login(nickname, password) {
    currentUser.value = await apiFetch('/auth/login', {
        method: 'POST',
        body: { nickname: nickname.trim(), password },
    })
    authState.value = AuthState.AUTHENTICATED
}


// Регистрация. Бэкенд НЕ логинит - после успеха форма сама переключит на вход.
// Бросает ApiError (409 - ник занят, 400 - пароли не совпали, 422 - политика пароля).
export async function register(nickname, password, repeatPassword) {
    await apiFetch('/auth/register', {
        method: 'POST',
        body: {
            nickname: nickname.trim(),
            password,
            repeat_password: repeatPassword,
        },
    })
}


// Выход по инициативе пользователя. Локальное состояние чистим всегда,
// даже если запрос не прошёл (кука уже могла протухнуть).
export async function logout() {
    try {
        await apiFetch('/auth/logout', { method: 'POST' })
    } catch {
        // игнорируем - локально всё равно выходим
    }
    currentUser.value = null
    authState.value = AuthState.ANONYMOUS
}


// Сессию оборвал сервер (401 на защищённой ручке). Вызывается из HTTP-слоёв
// потребителей (useShortener и т.п.).
export function handleUnauthorized() {
    if (authState.value !== AuthState.AUTHENTICATED) return
    currentUser.value = null
    authState.value = AuthState.EXPIRED
}


// Проверяем сессию сразу при загрузке модуля (один раз на жизнь вкладки)
fetchSession()
