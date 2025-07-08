<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-white font-medium">İş Akış Diyagramı</h4>
      <div v-if="data" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
        {{ data.steps.length }} adım tanımlandı
      </div>
    </div>
    <div ref="chartContainer" class="w-full h-96 bg-white rounded-lg"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  data: Object
})

const emit = defineEmits(['chart-ready'])

const chartContainer = ref(null)

const createChart = async () => {
  if (!chartContainer.value) return

  try {
    if (!window.mermaid) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
      document.head.appendChild(script)

      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
    }

    window.mermaid.initialize({
      startOnLoad: false,
      theme: 'default'
    })

    let definition

    if (props.data && props.data.steps.length > 0) {
      const steps = props.data.steps
      const connections = props.data.connections || []

      let nodes = steps.map(step => `    ${step.id}[${step.title}]`).join('\n')
      let edges = connections.map(conn => `    ${conn.from} --> ${conn.to}`).join('\n')
      let styles = steps.map(step => `    style ${step.id} fill:${step.color},stroke:${step.color},color:#fff`).join('\n')

      definition = `
flowchart LR
${nodes}
${edges}
${styles}
`
    } else {
      definition = `
flowchart LR
    A[Proje Başlangıcı] --> B[Gereksinim Toplama]
    B --> C[Analiz ve Tasarım]
    C --> D[Geliştirme]
    D --> E[Test]
    E --> F{Test Başarılı?}
    F -->|Evet| G[Deployment]
    F -->|Hayır| D
    G --> H[Bakım ve Destek]

    style A fill:#3b82f6,stroke:#2563eb,color:#fff
    style G fill:#10b981,stroke:#059669,color:#fff
    style F fill:#f59e0b,stroke:#d97706,color:#fff
    style H fill:#8b5cf6,stroke:#7c3aed,color:#fff
`
    }

    chartContainer.value.innerHTML = ''
    const { svg } = await window.mermaid.render('workflow-chart-' + Date.now(), definition)
    chartContainer.value.innerHTML = svg

    emit('chart-ready', chartContainer.value)
  } catch (error) {
    console.error('Mermaid render error:', error)
    chartContainer.value.innerHTML = '<div class="text-red-500 p-4">Şema yüklenemedi</div>'
  }
}

onMounted(createChart)
watch(() => props.data, createChart, { deep: true })
</script>
