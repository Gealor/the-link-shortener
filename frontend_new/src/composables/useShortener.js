import { ref } from 'vue'

const API_URL = 'http://localhost:8000/api'

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
      const res = await fetch(`${API_URL}/short-url`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ full_url: u })
      })
      if (!res.ok) {
        const e = await res.json()
        throw new Error(e.detail || 'Ошибка сервера')
      }
      result.value = await res.json()
    } catch (e) {
      error.value = e.message
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
