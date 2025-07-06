<template>
  <div class="flex flex-col h-full bg-gray-900/50">
    <!-- Header -->
    <div class="bg-gray-800/80 backdrop-blur-md border-b border-gray-700/50 shadow-lg">
      <div class="px-6 py-4 h-[80px] ">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-gradient-to-r from-emerald-600 to-teal-700 rounded-xl shadow-lg">
              <DocumentTextIcon class="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 class="text-lg font-semibold text-white">Proje Analiz Dokümanı</h2>
              <p class="text-xs text-gray-300">Sohbet geçmişinize dayalı analiz</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <!-- Download Dropdown -->
            <div class="relative" ref="downloadDropdown">
              <button
                @click="toggleDownloadMenu"
                class="flex items-center space-x-1 px-3 py-2 bg-gray-700 border border-gray-600 hover:border-gray-400 text-white rounded-lg transition-colors text-sm"
              >
                <ArrowDownTrayIcon class="w-4 h-4" />
                <span>İndir</span>
                <ChevronDownIcon class="w-3 h-3" />
              </button>

              <!-- Dropdown Menu -->
              <div v-show="showDownloadMenu" class="absolute right-0 mt-2 w-48 bg-gray-800 border border-gray-700 rounded-lg shadow-xl z-50">
                <div class="py-1">
                  <button
                    @click="downloadPDF"
                    :disabled="isGeneratingPDF"
                    class="flex items-center space-x-2 w-full px-4 py-2 text-left text-sm text-gray-300 border border-transparent hover:border-gray-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <DocumentIcon class="w-4 h-4" />
                    <span>{{ isGeneratingPDF ? 'PDF oluşturuluyor...' : 'PDF (.pdf)' }}</span>
                  </button>
                  <button
                    @click="downloadWord"
                    :disabled="isGeneratingWord"
                    class="flex items-center space-x-2 w-full px-4 py-2 text-left text-sm text-gray-300 border border-transparent hover:border-gray-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <DocumentTextIcon class="w-4 h-4" />
                    <span>{{ isGeneratingWord ? 'Word oluşturuluyor...' : 'Word (.docx)' }}</span>
                  </button>
                </div>
              </div>
            </div>

            <button
              @click="copyToClipboard"
              class="flex items-center space-x-1 px-3 py-2 bg-gray-700 border border-gray-600 hover:border-gray-400 text-white rounded-lg transition-colors text-sm"
            >
              <ClipboardDocumentIcon class="w-4 h-4" />
              <span>Kopyala</span>
            </button>
            <button
              @click="$emit('close-document')"
              class="p-2 text-gray-400 border border-transparent hover:border-gray-500 rounded-lg transition-colors"
            >
              <XMarkIcon class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Görsel Öğeler Tıklanabilir Alan -->
    <div class="border-b border-gray-700/50">
      <button
        @click="showVisualComponents = !showVisualComponents"
        class="w-full px-6 py-4 bg-gray-800/40 hover:bg-gray-800/60 border-b border-gray-700/30 transition-all duration-300 group"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="p-2 bg-gradient-to-r from-purple-600 to-pink-700 rounded-lg group-hover:scale-110 transition-transform duration-200">
              <ChartBarIcon class="w-5 h-5 text-white" />
            </div>
            <div class="text-left">
              <h3 class="text-white font-medium">Görsel Öğeler ve Analizler</h3>
              <p class="text-gray-400 text-sm">
                {{ visualData ? 'Dinamik verilerle oluşturulmuş grafikler ve şemalar' : 'Grafikler, şemalar ve analiz görselleri' }}
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <div v-if="visualData" class="px-2 py-1 bg-emerald-600/20 text-emerald-400 rounded text-xs">
              Dinamik
            </div>
            <span class="text-xs text-gray-500">
              {{ showVisualComponents ? 'Gizle' : 'Göster' }}
            </span>
            <div
              :class="[
                'transform transition-transform duration-300',
                showVisualComponents ? 'rotate-180' : 'rotate-0'
              ]"
            >
              <ChevronDownIcon class="w-4 h-4 text-gray-400" />
            </div>
          </div>
        </div>
      </button>

      <!-- Görsel Öğeler İçeriği -->
      <div
        :class="[
          'overflow-hidden transition-all duration-500 ease-in-out',
          showVisualComponents ? 'max-h-[600px] opacity-100' : 'max-h-0 opacity-0'
        ]"
      >
        <div class="p-6 bg-gray-800/20">
          <VisualComponents
            :visual-data="visualData"
            @close="showVisualComponents = false"
          />
        </div>
      </div>
    </div>

    <!-- Document Content -->
    <div class="flex-1 overflow-hidden">
      <div v-if="isLoading" class="flex items-center justify-center h-full">
        <div class="text-center">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
          <p class="mt-4 text-gray-400 text-sm">Doküman yükleniyor...</p>
        </div>
      </div>

      <div v-else-if="error" class="flex items-center justify-center h-full">
        <div class="text-center">
          <ExclamationTriangleIcon class="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 class="text-lg font-semibold text-white mb-2">Hata Oluştu</h3>
          <p class="text-gray-400 text-sm">{{ error }}</p>
        </div>
      </div>

      <div v-else class="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
        <div class="p-6">
          <!-- Rendered markdown content -->
          <div
            ref="documentContent"
            v-html="renderedMarkdown"
            class="markdown-content"
          ></div>
        </div>
      </div>
    </div>

    <!-- Notification -->
    <div
      v-if="notification.show"
      :class="[
        'fixed top-4 right-4 px-4 py-2 rounded-lg shadow-lg transition-all duration-300 z-50',
        notification.type === 'success' ? 'bg-green-600 text-white' : 'bg-red-600 text-white'
      ]"
    >
      {{ notification.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, watch, onMounted, onUnmounted } from 'vue'
import {
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ClipboardDocumentIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
  ChevronDownIcon,
  DocumentIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'
import VisualComponents from './VisualComponents.vue'

const props = defineProps({
  documentContent: {
    type: String,
    default: ''
  },
  sessionId: {
    type: String,
    default: ''
  },
  visualData: {
    type: Object,
    default: () => null
  }
})

defineEmits(['close-document'])

const isLoading = ref(false)
const error = ref('')
const isGeneratingPDF = ref(false)
const isGeneratingWord = ref(false)
const showDownloadMenu = ref(false)
const showVisualComponents = ref(false)
const downloadDropdown = ref(null)
const documentContent = ref(null)

const notification = ref({
  show: false,
  message: '',
  type: 'success'
})

// Advanced markdown to HTML converter
const parseMarkdown = (markdown) => {
  if (!markdown) return ''

  let html = markdown

  // Headers with proper hierarchy
  html = html.replace(/^### (.*$)/gm, '<h3 class="markdown-h3">$1</h3>')
  html = html.replace(/^## (.*$)/gm, '<h2 class="markdown-h2">$1</h2>')
  html = html.replace(/^# (.*$)/gm, '<h1 class="markdown-h1">$1</h1>')

  // Bold and italic
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="markdown-strong">$1</strong>')
  html = html.replace(/\*(.*?)\*/g, '<em class="markdown-em">$1</em>')

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code class="markdown-code">$1</code>')

  // Code blocks
  html = html.replace(/```([^`]+)```/g, '<pre class="markdown-pre"><code class="markdown-code-block">$1</code></pre>')

  // Tables - Enhanced table parsing
  const tableRegex = /(\|[^\n]+\|\n)+/g
  html = html.replace(tableRegex, (match) => {
    const rows = match.trim().split('\n')
    let tableHtml = '<table class="markdown-table">'

    rows.forEach((row, index) => {
      if (row.includes('|')) {
        const cells = row.split('|').filter(cell => cell.trim())
        if (index === 0) {
          // Header row
          tableHtml += '<thead><tr class="markdown-table-header">'
          cells.forEach(cell => {
            tableHtml += `<th class="markdown-th">${cell.trim()}</th>`
          })
          tableHtml += '</tr></thead><tbody>'
        } else {
          // Data row
          tableHtml += '<tr class="markdown-table-row">'
          cells.forEach(cell => {
            tableHtml += `<td class="markdown-td">${cell.trim()}</td>`
          })
          tableHtml += '</tr>'
        }
      }
    })

    tableHtml += '</tbody></table>'
    return tableHtml
  })

  // Lists - Unordered
  html = html.replace(/^\s*[-*+]\s+(.+)$/gm, '<li class="markdown-li">$1</li>')
  html = html.replace(/(<li class="markdown-li">.*<\/li>)/s, '<ul class="markdown-ul">$1</ul>')

  // Lists - Ordered
  html = html.replace(/^\s*\d+\.\s+(.+)$/gm, '<li class="markdown-li-ordered">$1</li>')
  html = html.replace(/(<li class="markdown-li-ordered">.*<\/li>)/s, '<ol class="markdown-ol">$1</ol>')

  // Blockquotes
  html = html.replace(/^>\s(.+)$/gm, '<blockquote class="markdown-blockquote">$1</blockquote>')

  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr class="markdown-hr">')

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="markdown-link" target="_blank" rel="noopener noreferrer">$1</a>')

  // Line breaks and paragraphs
  html = html.replace(/\n\n/g, '</p><p class="markdown-p">')
  html = html.replace(/^(?!<[h|u|o|l|t|b|p])/gm, '<p class="markdown-p">')
  html = html.replace(/(?<![>])$/gm, '</p>')

  // Clean up empty paragraphs and fix nesting
  html = html.replace(/<p class="markdown-p"><\/p>/g, '')
  html = html.replace(/<p class="markdown-p">(<[h|u|o|l|t|b])/g, '$1')
  html = html.replace(/(<\/[h|u|o|l|t|b]>)<\/p>/g, '$1')

  return html
}

const renderedMarkdown = computed(() => {
  return parseMarkdown(props.documentContent)
})

const showNotification = (message, type = 'success') => {
  notification.value = { show: true, message, type }
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

const toggleDownloadMenu = () => {
  showDownloadMenu.value = !showDownloadMenu.value
}

const copyToClipboard = async () => {
  try {
    await navigator.clipboard.writeText(props.documentContent)
    showNotification('Doküman panoya kopyalandı!', 'success')
  } catch (err) {
    showNotification('Kopyalama işlemi başarısız oldu', 'error')
  }
}

const generateHTMLTemplate = (content) => {
  return `<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proje Analiz Dokümanı</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }

        .header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #007bff;
        }

        .header h1 {
            color: #007bff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .header .date {
            color: #666;
            font-style: italic;
        }

        .markdown-h1 {
            color: #2c3e50;
            font-size: 2em;
            margin: 30px 0 20px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }

        .markdown-h2 {
            color: #3498db;
            font-size: 1.5em;
            margin: 25px 0 15px 0;
        }

        .markdown-h3 {
            color: #27ae60;
            font-size: 1.2em;
            margin: 20px 0 10px 0;
        }

        .markdown-p {
            margin-bottom: 15px;
            text-align: justify;
        }

        .markdown-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .markdown-th {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 1px solid #2980b9;
        }

        .markdown-td {
            padding: 12px 15px;
            border-bottom: 1px solid #ecf0f1;
            vertical-align: top;
        }

        .markdown-table-row:nth-child(even) {
            background-color: #f8f9fa;
        }

        .markdown-table-row:hover {
            background-color: #e3f2fd;
        }

        .markdown-strong {
            font-weight: 600;
            color: #2c3e50;
        }

        .markdown-em {
            font-style: italic;
            color: #7f8c8d;
        }

        .markdown-code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #e74c3c;
        }

        .markdown-ul, .markdown-ol {
            margin: 15px 0;
            padding-left: 30px;
        }

        .markdown-li {
            margin-bottom: 8px;
        }

        .markdown-blockquote {
            border-left: 4px solid #3498db;
            background: #f8f9fa;
            padding: 15px 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
            font-style: italic;
        }

        .markdown-hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #2ecc71);
            margin: 30px 0;
            border-radius: 1px;
        }

        .markdown-link {
            color: #3498db;
            text-decoration: none;
            border-bottom: 1px dotted #3498db;
        }

        .markdown-link:hover {
            color: #2980b9;
            border-bottom: 1px solid #2980b9;
        }

        @media print {
            body {
                background: white;
                padding: 0;
            }

            .container {
                box-shadow: none;
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Proje Analiz Dokümanı</h1>
            <div class="date">Oluşturulma Tarihi: ${new Date().toLocaleDateString('tr-TR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })}</div>
        </div>
        ${content}
    </div>
</body>
</html>`
}

const downloadWord = async () => {
  showNotification('Word indirme özelliği henüz aktif değil', 'error')
  showDownloadMenu.value = false
}

const downloadPDF = async () => {
  if (!props.documentContent) return

  isGeneratingPDF.value = true

  try {
    // Create a temporary window for PDF generation
    const printWindow = window.open('', '_blank')
    const htmlContent = generateHTMLTemplate(renderedMarkdown.value)

    printWindow.document.write(htmlContent)
    printWindow.document.close()

    // Wait for content to load
    await new Promise(resolve => {
      printWindow.onload = resolve
      setTimeout(resolve, 1000) // Fallback timeout
    })

    // Trigger print dialog
    printWindow.print()

    // Close the temporary window after printing
    setTimeout(() => {
      printWindow.close()
    }, 1000)

    showNotification('PDF yazdırma penceresi açıldı!', 'success')
  } catch (error) {
    console.error('PDF generation error:', error)
    showNotification('PDF oluşturulurken hata oluştu', 'error')
  } finally {
    isGeneratingPDF.value = false
    showDownloadMenu.value = false
  }
}

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (downloadDropdown.value && !downloadDropdown.value.contains(event.target)) {
    showDownloadMenu.value = false
  }
}

// Props değişikliklerini izle
watch(() => props.documentContent, (newContent) => {
  if (newContent) {
    isLoading.value = false
    error.value = ''
  }
}, { immediate: true })

// Visual data değişikliklerini izle ve otomatik olarak göster
watch(() => props.visualData, (newVisualData) => {
  if (newVisualData) {
    showVisualComponents.value = true
  }
}, { immediate: true })

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: rgb(75 85 99);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: rgb(107 114 128);
}

.markdown-content {
  color: #f3f4f6;
  line-height: 1.7;
}

/* Headers */
.markdown-content :deep(.markdown-h1) {
  color: #ffffff;
  font-size: 1.875rem;
  font-weight: 700;
  margin: 2rem 0 1.5rem 0;
  padding-bottom: 0.75rem;
  border-bottom: 3px solid #3b82f6;
  position: relative;
}

.markdown-content :deep(.markdown-h1:first-child) {
  margin-top: 0;
}

.markdown-content :deep(.markdown-h1::before) {
  content: '📋';
  margin-right: 0.5rem;
}

.markdown-content :deep(.markdown-h2) {
  color: #60a5fa;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 2rem 0 1rem 0;
  position: relative;
  padding-left: 1rem;
}

.markdown-content :deep(.markdown-h2::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(to bottom, #3b82f6, #1d4ed8);
  border-radius: 2px;
}

.markdown-content :deep(.markdown-h3) {
  color: #34d399;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 1.5rem 0 0.75rem 0;
  display: flex;
  align-items: center;
}

.markdown-content :deep(.markdown-h3::before) {
  content: '▶';
  margin-right: 0.5rem;
  color: #10b981;
  font-size: 0.8em;
}

/* Paragraphs */
.markdown-content :deep(.markdown-p) {
  color: #e5e7eb;
  margin-bottom: 1rem;
  line-height: 1.7;
  text-align: justify;
}

/* Tables */
.markdown-content :deep(.markdown-table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: rgba(31, 41, 55, 0.8);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(75, 85, 99, 0.3);
}

.markdown-content :deep(.markdown-table-header) {
  background: linear-gradient(135deg, #374151, #4b5563);
}

.markdown-content :deep(.markdown-th) {
  color: #ffffff;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  font-size: 0.875rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  border-bottom: 2px solid #4b5563;
  position: relative;
}

.markdown-content :deep(.markdown-th:not(:last-child)::after) {
  content: '';
  position: absolute;
  right: 0;
  top: 25%;
  bottom: 25%;
  width: 1px;
  background: rgba(156, 163, 175, 0.3);
}

.markdown-content :deep(.markdown-td) {
  color: #f3f4f6;
  padding: 0.875rem 1rem;
  border-bottom: 1px solid rgba(75, 85, 99, 0.2);
  font-size: 0.875rem;
  vertical-align: top;
  position: relative;
}

.markdown-content :deep(.markdown-table-row) {
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.markdown-content :deep(.markdown-table-row:nth-child(even)) {
  background-color: rgba(55, 65, 81, 0.3);
}

.markdown-content :deep(.markdown-table-row:hover) {
  border-color: rgba(59, 130, 246, 0.5);
}

.markdown-content :deep(.markdown-td:not(:last-child)::after) {
  content: '';
  position: absolute;
  right: 0;
  top: 10%;
  bottom: 10%;
  width: 1px;
  background: rgba(107, 114, 128, 0.2);
}

/* Text formatting */
.markdown-content :deep(.markdown-strong) {
  color: #ffffff;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.markdown-content :deep(.markdown-em) {
  color: #d1d5db;
  font-style: italic;
}

.markdown-content :deep(.markdown-code) {
  color: #34d399;
  background: rgba(31, 41, 55, 0.8);
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
  font-size: 0.875em;
  border: 1px solid rgba(52, 211, 153, 0.2);
  box-shadow: 0 2px 8px rgba(52, 211, 153, 0.1);
}

.markdown-content :deep(.markdown-pre) {
  background: rgba(17, 24, 39, 0.9);
  padding: 1.5rem;
  border-radius: 12px;
  margin: 1.5rem 0;
  border: 1px solid rgba(75, 85, 99, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  overflow-x: auto;
}

.markdown-content :deep(.markdown-code-block) {
  color: #e5e7eb;
  background: transparent;
  padding: 0;
  border: none;
  box-shadow: none;
  font-size: 0.875rem;
  line-height: 1.6;
}

/* Lists */
.markdown-content :deep(.markdown-ul),
.markdown-content :deep(.markdown-ol) {
  margin: 1rem 0;
  padding-left: 2rem;
}

.markdown-content :deep(.markdown-li) {
  color: #e5e7eb;
  margin-bottom: 0.5rem;
  line-height: 1.6;
  position: relative;
}

.markdown-content :deep(.markdown-ul .markdown-li::before) {
  content: '•';
  color: #3b82f6;
  font-weight: bold;
  position: absolute;
  left: -1.5rem;
}

.markdown-content :deep(.markdown-li-ordered) {
  color: #e5e7eb;
  margin-bottom: 0.5rem;
  line-height: 1.6;
}

/* Blockquotes */
.markdown-content :deep(.markdown-blockquote) {
  border-left: 4px solid #3b82f6;
  background: rgba(31, 41, 55, 0.6);
  padding: 1.5rem;
  margin: 1.5rem 0;
  border-radius: 0 12px 12px 0;
  color: #d1d5db;
  font-style: italic;
  position: relative;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.1);
}

.markdown-content :deep(.markdown-blockquote::before) {
  content: '"';
  position: absolute;
  top: 0.5rem;
  left: 1rem;
  font-size: 2rem;
  color: #3b82f6;
  opacity: 0.5;
}

/* Horizontal rules */
.markdown-content :deep(.markdown-hr) {
  border: none;
  height: 2px;
  background: linear-gradient(to right, #3b82f6, #10b981);
  margin: 2rem 0;
  border-radius: 1px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* Links */
.markdown-content :deep(.markdown-link) {
  color: #60a5fa;
  text-decoration: none;
  border-bottom: 1px dotted #60a5fa;
  transition: all 0.2s ease;
}

.markdown-content :deep(.markdown-link:hover) {
  color: #3b82f6;
  border-bottom: 1px solid #3b82f6;
  text-shadow: 0 0 8px rgba(59, 130, 246, 0.3);
}

/* Animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.markdown-content :deep(.markdown-table),
.markdown-content :deep(.markdown-blockquote),
.markdown-content :deep(.markdown-pre) {
  animation: fadeIn 0.3s ease-out;
}

/* Print styles */
@media print {
  .markdown-content :deep(.markdown-table) {
    background: white !important;
    color: black !important;
    border: 1px solid #ccc !important;
  }

  .markdown-content :deep(.markdown-th) {
    background: #f5f5f5 !important;
    color: black !important;
  }

  .markdown-content :deep(.markdown-td) {
    color: black !important;
  }
}
</style>
