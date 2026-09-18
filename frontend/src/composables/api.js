const API_URL = import.meta.env.VITE_API_URL

// Double-submit CSRF-токен. Живёт только в памяти вкладки (не localStorage) -
// источник правды - HttpOnly-кука на бэкенде, этот токен - её "расшифрованная"
// пара для заголовка. Заполняется/чистится через setCsrfToken из auth.js
// (после login/me и logout соответственно).
let csrfToken = null

export function setCsrfToken(token) {
    csrfToken = token
}

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS'])


// Ошибка обращения к API.
// status === 0 - запрос не дошёл (сеть/сервер недоступен).
// message - текст для показа пользователю.
// isCsrfError - true, если 403 конкретно из-за CSRF-проверки (сервер шлёт заголовок
// X-CSRF-Error) - отличает от других 403 (например, "аккаунт заблокирован" на /auth/login),
// чтобы не парсить текст detail на фронте.
export class ApiError extends Error {
    constructor(status, message, isCsrfError = false) {
        super(message)
        this.name = 'ApiError'
        this.status = status
        this.isCsrfError = isCsrfError
    }
}

const DEFAULT_MESSAGES = {
    0: 'Cannot reach the server. Is it running?',
    500: 'Something went wrong on the server.',
}

function messageFromBody(body, status) {
    if (status >= 500) return DEFAULT_MESSAGES[500]

    const detail = body?.detail
    if (typeof detail === 'string' && detail) return detail
    // 422 от pydantic: {detail: [{msg, loc}, ...]}
    if (Array.isArray(detail) && typeof detail[0]?.msg === 'string') return detail[0].msg

    return `Request failed (${status}).`
}


// Бросает ApiError на любой не-2xx ответ и на сетевой сбой.
// Возвращает распарсенный JSON (или null для пустого тела).
export async function apiFetch(path, { method = 'GET', body } = {}) {
    const headers = { Accept: 'application/json' }
    const init = { method, headers, credentials: 'include'}

    if (csrfToken && !SAFE_METHODS.has(method.toUpperCase())) {
        headers['X-CSRF-Token'] = csrfToken
    }

    if (body !== undefined) {
        headers['Content-Type'] = 'application/json'
        init.body = JSON.stringify(body)
    }

    let res
    try {
        res = await fetch(`${API_URL}${path}`, init)
    } catch (e) {
        if (e.name === 'AbortError') throw e
        throw new ApiError(0, DEFAULT_MESSAGES[0])
    }

    const payload = res.status === 204 ? null : await res.json().catch(() => null)

    if (!res.ok) {
        throw new ApiError(res.status, messageFromBody(payload, res.status), res.headers.has('X-CSRF-Error'))
    }

    return payload
}
