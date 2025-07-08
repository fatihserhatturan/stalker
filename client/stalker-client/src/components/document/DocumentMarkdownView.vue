<template>
  <div class="h-full overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-transparent">
    <div class="p-6">
      <div
        ref="documentContent"
        v-html="renderedMarkdown"
        class="markdown-content"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useMarkdown } from '@/composables/useMarkdown'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

const { parseMarkdown } = useMarkdown()
const documentContent = ref(null)

const renderedMarkdown = computed(() => {
  return parseMarkdown(props.content)
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

.markdown-content :deep(.markdown-p) {
  color: #e5e7eb;
  margin-bottom: 1rem;
  line-height: 1.7;
  text-align: justify;
}

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

.markdown-content :deep(.markdown-hr) {
  border: none;
  height: 2px;
  background: linear-gradient(to right, #3b82f6, #10b981);
  margin: 2rem 0;
  border-radius: 1px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.markdown-content :deep(.markdown-table),
.markdown-content :deep(.markdown-blockquote),
.markdown-content :deep(.markdown-pre) {
  animation: fadeIn 0.3s ease-out;
}

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
