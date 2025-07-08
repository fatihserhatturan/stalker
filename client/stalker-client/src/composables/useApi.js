import { ref } from 'vue'

const API_BASE_URL = 'http://localhost:8000'

export function useApi() {
  const isLoading = ref(false)
  const error = ref(null)

  const makeRequest = async (url, options = {}) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
      }

      return await response.json()
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const get = (url, options = {}) => makeRequest(url, { method: 'GET', ...options })
  const post = (url, data, options = {}) => makeRequest(url, {
    method: 'POST',
    body: JSON.stringify(data),
    ...options,
  })
  const upload = (url, formData) => makeRequest(url, {
    method: 'POST',
    body: formData,
    headers: {},
  })

  return {
    isLoading,
    error,
    get,
    post,
    upload,
  }
}
