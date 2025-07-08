import { ref } from 'vue'
import { useApi } from './useApi'

export function useDocument() {
  const { get, post } = useApi()

  const sessionDocuments = ref([])
  const isGenerating = ref(false)
  const documentContent = ref('')
  const visualData = ref(null)

  const loadSessionDocuments = async (sessionId) => {
    try {
      const response = await get(`/session-documents/${sessionId}`)
      sessionDocuments.value = response.documents || []
      return response.documents
    } catch (error) {
      console.error('Error loading session documents:', error)
      return []
    }
  }

  const loadDocument = async (sessionId, documentId) => {
    try {
      const response = await get(`/document/${sessionId}/${documentId}`)
      return response.document
    } catch (error) {
      console.error('Error loading document:', error)
      throw error
    }
  }

  const generateAnalysisDocument = async (sessionId, useTemplate = false) => {
    isGenerating.value = true

    try {
      const response = await post('/generate-analysis-document', {
        session_id: sessionId,
        use_template: useTemplate
      })

      documentContent.value = response.document_content
      await loadSessionDocuments(sessionId)

      return response
    } finally {
      isGenerating.value = false
    }
  }

  const generateVisualData = async (sessionId) => {
    try {
      const response = await post('/generate-visual-data', {
        session_id: sessionId,
        message: "generate_visual_data"
      })

      visualData.value = response.visual_data
      return response.visual_data
    } catch (error) {
      console.error('Error generating visual data:', error)
      visualData.value = null
      return null
    }
  }

  const clearDocument = () => {
    documentContent.value = ''
  }

  const clearVisualData = () => {
    visualData.value = null
  }

  return {
    sessionDocuments,
    isGenerating,
    documentContent,
    visualData,
    loadSessionDocuments,
    loadDocument,
    generateAnalysisDocument,
    generateVisualData,
    clearDocument,
    clearVisualData,
  }
}
