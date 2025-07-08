import { ref } from 'vue'
import { useMarkdown } from './useMarkdown'
import { useNotifications } from './useNotifications'

export function useDocumentExport() {
  const { parseMarkdown, generateHTMLTemplate } = useMarkdown()
  const { showNotification } = useNotifications()

  const isGeneratingPDF = ref(false)
  const isGeneratingWord = ref(false)

  const copyToClipboard = async (content) => {
    try {
      await navigator.clipboard.writeText(content)
      showNotification('Doküman panoya kopyalandı!', 'success')
    } catch (err) {
      showNotification('Kopyalama işlemi başarısız oldu', 'error')
    }
  }

  const downloadPDF = async (documentContent) => {
    if (!documentContent) return

    isGeneratingPDF.value = true

    try {
      const renderedMarkdown = parseMarkdown(documentContent)
      const htmlContent = generateHTMLTemplate(renderedMarkdown)

      const printWindow = window.open('', '_blank')
      printWindow.document.write(htmlContent)
      printWindow.document.close()

      await new Promise(resolve => {
        printWindow.onload = resolve
        setTimeout(resolve, 1000)
      })

      printWindow.print()

      setTimeout(() => {
        printWindow.close()
      }, 1000)

      showNotification('PDF yazdırma penceresi açıldı!', 'success')
    } catch (error) {
      console.error('PDF generation error:', error)
      showNotification('PDF oluşturulurken hata oluştu', 'error')
    } finally {
      isGeneratingPDF.value = false
    }
  }

  const downloadWord = async () => {
    showNotification('Word indirme özelliği henüz aktif değil', 'error')
  }

  return {
    isGeneratingPDF,
    isGeneratingWord,
    copyToClipboard,
    downloadPDF,
    downloadWord
  }
}
