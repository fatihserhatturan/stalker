import { ref } from 'vue'
import { useApi } from './useApi'

export function useFileUpload() {
  const { upload } = useApi()

  const selectedFile = ref(null)
  const templateFile = ref(null)
  const isUploading = ref(false)

  const validateFile = (file, options = {}) => {
    const {
      maxSize = 10 * 1024 * 1024,
      allowedTypes = ['text/plain', 'text/markdown', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword'],
      allowedExtensions = ['.txt', '.md', '.pdf', '.docx', '.doc']
    } = options

    if (file.size > maxSize) {
      throw new Error(`Dosya boyutu ${maxSize / (1024 * 1024)}MB'dan büyük olamaz`)
    }

    const fileExtension = '.' + file.name.split('.').pop().toLowerCase()

    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      throw new Error(`Desteklenmeyen dosya formatı. İzin verilen formatlar: ${allowedExtensions.join(', ')}`)
    }

    return true
  }

  const uploadProjectFile = async (file, sessionId) => {
    validateFile(file)

    isUploading.value = true

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('session_id', sessionId)

      const response = await upload('/upload-file', formData)
      selectedFile.value = null

      return response
    } finally {
      isUploading.value = false
    }
  }

  const uploadTemplate = async (file, sessionId) => {
    validateFile(file, { maxSize: 5 * 1024 * 1024 })

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('session_id', sessionId)
      formData.append('is_template', 'true')

      const response = await upload('/upload-template', formData)
      templateFile.value = file

      return response
    } catch (error) {
      templateFile.value = null
      throw error
    }
  }

  const setSelectedFile = (file) => {
    validateFile(file)
    selectedFile.value = file
  }

  const setTemplateFile = (file) => {
    validateFile(file, { maxSize: 5 * 1024 * 1024 })
    templateFile.value = file
  }

  const removeSelectedFile = () => {
    selectedFile.value = null
  }

  const removeTemplate = () => {
    templateFile.value = null
  }

  return {
    selectedFile,
    templateFile,
    isUploading,
    setSelectedFile,
    setTemplateFile,
    removeSelectedFile,
    removeTemplate,
    uploadProjectFile,
    uploadTemplate,
    validateFile,
  }
}
