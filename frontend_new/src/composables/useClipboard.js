import { ref } from 'vue'

export function useClipboard() {
  const copied = ref('')
  const toast = ref('')

  function showToast(msg) {
    toast.value = msg
    setTimeout(() => { toast.value = '' }, 2000)
  }

  async function copy(text, key) {
    try {
      await navigator.clipboard.writeText(text)
    } catch {
      // Fallback для старых браузеров
      const ta = document.createElement('textarea')
      ta.value = text
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
    }
    copied.value = key
    showToast('Скопировано в буфер обмена!')
    setTimeout(() => { copied.value = '' }, 2000)
  }

  return { copied, toast, copy }
}
