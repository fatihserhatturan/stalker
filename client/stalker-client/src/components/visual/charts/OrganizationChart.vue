<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-white font-medium">Proje Organizasyon Şeması</h4>
      <div v-if="data" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
        {{ data.roles.length }} rol tanımlandı
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
      theme: 'default',
      themeVariables: {
        primaryColor: '#3b82f6',
        primaryTextColor: '#1f2937',
        primaryBorderColor: '#2563eb',
        lineColor: '#6b7280',
        secondaryColor: '#e5e7eb',
        tertiaryColor: '#f3f4f6'
      }
    })

    let definition

    if (props.data && props.data.roles.length > 0) {
      const roles = props.data.roles
      const connections = props.data.connections || []

      let nodes = roles.map(role => `    ${role.id}[${role.title}]`).join('\n')
      let edges = connections.map(conn => `    ${conn.from} --> ${conn.to}`).join('\n')
      let styles = roles.map(role => `    style ${role.id} fill:${role.color},stroke:${role.color},color:#fff`).join('\n')

      definition = `
graph TD
${nodes}
${edges}
${styles}
`
    } else {
      definition = `
graph TD
    PM[Proje Müdürü] --> BA[İş Analisti]
    PM --> DEV[Geliştirme Ekibi]
    PM --> QA[Test Ekibi]

    BA --> REQ[Gereksinim Analizi]
    BA --> DOC[Dokümantasyon]

    DEV --> FE[Frontend Developer]
    DEV --> BE[Backend Developer]
    DEV --> DB[Veritabanı Uzmanı]

    QA --> UT[Unit Test]
    QA --> IT[Entegrasyon Test]
    QA --> UAT[Kullanıcı Kabul Test]

    style PM fill:#3b82f6,stroke:#2563eb,color:#fff
    style BA fill:#10b981,stroke:#059669,color:#fff
    style DEV fill:#f59e0b,stroke:#d97706,color:#fff
    style QA fill:#ef4444,stroke:#dc2626,color:#fff
`
    }

    chartContainer.value.innerHTML = ''
    const { svg } = await window.mermaid.render('org-chart-' + Date.now(), definition)
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
