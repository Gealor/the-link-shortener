import { ref } from 'vue'

import { ApiError, apiFetch } from './api.js'
import { handleUnauthorized } from './auth.js'

function validateUrl(u) {
  try { new URL(u); return true } catch { return false }
}

export function useShortener() {
  const url = ref('')
  const result = ref(null)
  const error = ref('')
  const loading = ref(false)

  async function shortenUrl() {
    error.value = ''
    const u = url.value.trim()

    if (!u) { error.value = 'Пожалуйста, введите URL'; return }
    if (!validateUrl(u)) { error.value = 'Введите корректный URL'; return }

    loading.value = true
    try {
      result.value = await apiFetch('/short-url', {
        method: 'POST',
        body: { full_url: u },
      })
    } catch (e) {
      if (!e instanceof ApiError) throw e
      // сессия оборвана сервером — выходим на экран логина, инлайн-ошибку не показываем
      if (e.status === 401) {
        handleUnauthorized()
        return
      }
      if (e.isCsrfError) {
        error.value = 'Please refresh the page and try again.'
      }
      else error.value = e.message
    } finally {
      loading.value = false
    }
  }

  function reset() {
    url.value = ''
    result.value = null
    error.value = ''
  }

  return { url, result, error, loading, shortenUrl, reset }
}
