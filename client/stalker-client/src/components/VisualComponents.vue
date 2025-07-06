<template>
  <div class="bg-gray-800/60 rounded-xl p-6 border border-gray-700/50">
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="p-2 bg-gradient-to-r from-purple-600 to-pink-700 rounded-lg">
          <ChartBarIcon class="w-5 h-5 text-white" />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-white">Görsel Analiz Araçları</h3>
          <p class="text-xs text-gray-400 mt-1">
            {{ visualData ? 'Konuşma verilerinize dayalı dinamik analizler' : 'Örnek analizler ve şemalar' }}
          </p>
        </div>
      </div>
      <div v-if="visualData" class="px-3 py-1 bg-emerald-600/20 text-emerald-400 rounded-full text-xs font-medium">
        Dinamik Veri
      </div>
    </div>

    <!-- Görsel Seçim Menüsü -->
    <div class="flex flex-wrap gap-3 mb-6">
      <button
        v-for="visual in visualTypes"
        :key="visual.id"
        @click="selectedVisual = visual.id"
        :class="[
          'flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-200 border',
          selectedVisual === visual.id
            ? 'bg-purple-600 border-purple-500 text-white'
            : 'bg-gray-700 border-gray-600 text-gray-300 hover:border-purple-500 hover:text-white'
        ]"
      >
        <component :is="visual.icon" class="w-4 h-4" />
        <span class="text-sm">{{ visual.name }}</span>
      </button>
    </div>

    <!-- Görsel İçerik Alanı -->
    <div class="bg-gray-900/50 rounded-lg p-4 min-h-[400px]">
      <!-- Proje Organizasyon Şeması -->
      <div v-if="selectedVisual === 'orgChart'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">Proje Organizasyon Şeması</h4>
          <div v-if="dynamicOrgData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicOrgData.roles.length }} rol tanımlandı
          </div>
        </div>
        <div ref="orgChartContainer" class="w-full h-96 bg-white rounded-lg"></div>
      </div>

      <!-- İş Akış Diyagramı -->
      <div v-if="selectedVisual === 'workflow'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">İş Akış Diyagramı</h4>
          <div v-if="dynamicWorkflowData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicWorkflowData.steps.length }} adım tanımlandı
          </div>
        </div>
        <div ref="workflowContainer" class="w-full h-96 bg-white rounded-lg"></div>
      </div>

      <!-- Proje Zaman Çizelgesi -->
      <div v-if="selectedVisual === 'timeline'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">Proje Zaman Çizelgesi</h4>
          <div v-if="dynamicTimelineData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicTimelineData.phases.length }} faz planlandı
          </div>
        </div>
        <canvas ref="timelineChart" class="w-full h-96 bg-white rounded-lg"></canvas>
      </div>

      <!-- Risk Analizi -->
      <div v-if="selectedVisual === 'riskAnalysis'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">Risk Analizi</h4>
          <div v-if="dynamicRiskData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicRiskData.risks.length }} risk tespit edildi
          </div>
        </div>
        <canvas ref="riskChart" class="w-full h-96 bg-white rounded-lg"></canvas>
      </div>

      <!-- Kaynak Dağılımı -->
      <div v-if="selectedVisual === 'resources'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">Kaynak Dağılımı</h4>
          <div v-if="dynamicResourceData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicResourceData.distribution.length }} kaynak türü
          </div>
        </div>
        <canvas ref="resourceChart" class="w-full h-96 bg-white rounded-lg"></canvas>
      </div>

      <!-- Maliyet Tahmini -->
      <div v-if="selectedVisual === 'cost'" class="space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-white font-medium">Maliyet Tahmini</h4>
          <div v-if="dynamicCostData" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
            {{ dynamicCostData.timeline.length }} aylık projeksiyon
          </div>
        </div>
        <canvas ref="costChart" class="w-full h-96 bg-white rounded-lg"></canvas>
      </div>
    </div>

    <!-- Veri Durumu Bilgisi -->
    <div v-if="!visualData" class="mt-4 p-3 bg-yellow-500/10 border border-yellow-500/20 rounded-lg">
      <div class="flex items-center space-x-2">
        <ExclamationTriangleIcon class="w-4 h-4 text-yellow-400" />
        <span class="text-xs text-yellow-400">
          Şu anda örnek verilerle gösterim yapılıyor. Dinamik veriler için analiz dokümanı oluşturun.
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import {
  ChartBarIcon,
  UserGroupIcon,
  CogIcon,
  ClockIcon,
  ExclamationTriangleIcon,
  CpuChipIcon,
  CurrencyDollarIcon
} from '@heroicons/vue/24/outline'

const props = defineProps({
  visualData: {
    type: Object,
    default: () => null
  }
})

const selectedVisual = ref('orgChart')

const visualTypes = [
  { id: 'orgChart', name: 'Organizasyon', icon: UserGroupIcon },
  { id: 'workflow', name: 'İş Akışı', icon: CogIcon },
  { id: 'timeline', name: 'Zaman Çizelgesi', icon: ClockIcon },
  { id: 'riskAnalysis', name: 'Risk Analizi', icon: ExclamationTriangleIcon },
  { id: 'resources', name: 'Kaynaklar', icon: CpuChipIcon },
  { id: 'cost', name: 'Maliyet', icon: CurrencyDollarIcon }
]

// Chart.js refs
const timelineChart = ref(null)
const riskChart = ref(null)
const resourceChart = ref(null)
const costChart = ref(null)

// Mermaid refs
const orgChartContainer = ref(null)
const workflowContainer = ref(null)

// Chart instances
let timelineChartInstance = null
let riskChartInstance = null
let resourceChartInstance = null
let costChartInstance = null

// Computed properties for dynamic data
const dynamicOrgData = computed(() => {
  if (!props.visualData?.orgChart) return null
  return props.visualData.orgChart
})

const dynamicWorkflowData = computed(() => {
  if (!props.visualData?.workflow) return null
  return props.visualData.workflow
})

const dynamicTimelineData = computed(() => {
  if (!props.visualData?.timeline) return null
  return props.visualData.timeline
})

const dynamicRiskData = computed(() => {
  if (!props.visualData?.riskAnalysis) return null
  return props.visualData.riskAnalysis
})

const dynamicResourceData = computed(() => {
  if (!props.visualData?.resources) return null
  return props.visualData.resources
})

const dynamicCostData = computed(() => {
  if (!props.visualData?.cost) return null
  return props.visualData.cost
})

const createMermaidChart = async (container, definition) => {
  if (!container) return

  try {
    // Create script element to load mermaid
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

    container.innerHTML = ''
    const { svg } = await window.mermaid.render('chart-' + Date.now(), definition)
    container.innerHTML = svg
  } catch (error) {
    console.error('Mermaid render error:', error)
    container.innerHTML = '<div class="text-red-500 p-4">Şema yüklenemedi</div>'
  }
}

const createOrgChart = async () => {
  await nextTick()
  if (!orgChartContainer.value) return

  let definition

  if (dynamicOrgData.value && dynamicOrgData.value.roles.length > 0) {
    // Dinamik veri kullan
    const roles = dynamicOrgData.value.roles
    const connections = dynamicOrgData.value.connections || []

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
    // Varsayılan veri kullan
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

  await createMermaidChart(orgChartContainer.value, definition)
}

const createWorkflowChart = async () => {
  await nextTick()
  if (!workflowContainer.value) return

  let definition

  if (dynamicWorkflowData.value && dynamicWorkflowData.value.steps.length > 0) {
    // Dinamik veri kullan
    const steps = dynamicWorkflowData.value.steps
    const connections = dynamicWorkflowData.value.connections || []

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
    // Varsayılan veri kullan
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

  await createMermaidChart(workflowContainer.value, definition)
}

const destroyChart = (chartInstance) => {
  if (chartInstance) {
    chartInstance.destroy()
    return null
  }
}

const createTimelineChart = async () => {
  await nextTick()
  if (!timelineChart.value) return

  try {
    // Load Chart.js if not already loaded
    if (!window.Chart) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
      document.head.appendChild(script)

      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
    }

    timelineChartInstance = destroyChart(timelineChartInstance)

    let chartData

    if (dynamicTimelineData.value && dynamicTimelineData.value.phases.length > 0) {
      // Dinamik veri kullan
      const phases = dynamicTimelineData.value.phases
      chartData = {
        labels: phases.map(phase => phase.name),
        datasets: [{
          label: 'Planlanan (Gün)',
          data: phases.map(phase => phase.planned),
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderColor: 'rgba(59, 130, 246, 1)',
          borderWidth: 1
        }, {
          label: 'Gerçekleşen (Gün)',
          data: phases.map(phase => phase.actual),
          backgroundColor: 'rgba(16, 185, 129, 0.8)',
          borderColor: 'rgba(16, 185, 129, 1)',
          borderWidth: 1
        }]
      }
    } else {
      // Varsayılan veri kullan
      chartData = {
        labels: ['Analiz', 'Tasarım', 'Geliştirme', 'Test', 'Deployment'],
        datasets: [{
          label: 'Planlanan (Gün)',
          data: [10, 15, 45, 20, 5],
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderColor: 'rgba(59, 130, 246, 1)',
          borderWidth: 1
        }, {
          label: 'Gerçekleşen (Gün)',
          data: [12, 18, 40, 25, 7],
          backgroundColor: 'rgba(16, 185, 129, 0.8)',
          borderColor: 'rgba(16, 185, 129, 1)',
          borderWidth: 1
        }]
      }
    }

    timelineChartInstance = new window.Chart(timelineChart.value, {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Proje Fazları - Zaman Karşılaştırması'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Gün'
            }
          }
        }
      }
    })
  } catch (error) {
    console.error('Chart.js load error:', error)
  }
}

const createRiskChart = async () => {
  await nextTick()
  if (!riskChart.value) return

  try {
    if (!window.Chart) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
      document.head.appendChild(script)
      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
    }

    riskChartInstance = destroyChart(riskChartInstance)

    let chartData

    if (dynamicRiskData.value && dynamicRiskData.value.risks.length > 0) {
      // Dinamik veri kullan
      const risks = dynamicRiskData.value.risks
      chartData = {
        datasets: [{
          label: 'Riskler',
          data: risks.map(risk => ({
            x: risk.probability,
            y: risk.impact,
            label: risk.name
          })),
          backgroundColor: risks.map(risk => risk.color || 'rgba(59, 130, 246, 0.8)'),
          pointRadius: 10
        }]
      }
    } else {
      // Varsayılan veri kullan
      chartData = {
        datasets: [{
          label: 'Riskler',
          data: [
            { x: 3, y: 4, label: 'Teknik Zorluklar' },
            { x: 2, y: 3, label: 'Kaynak Eksikliği' },
            { x: 4, y: 2, label: 'Zaman Kısıtı' },
            { x: 1, y: 5, label: 'Güvenlik Açıkları' },
            { x: 3, y: 3, label: 'Entegrasyon Sorunları' }
          ],
          backgroundColor: [
            'rgba(239, 68, 68, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(59, 130, 246, 0.8)'
          ],
          pointRadius: 10
        }]
      }
    }

    riskChartInstance = new window.Chart(riskChart.value, {
      type: 'scatter',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Risk Analizi - Olasılık vs Etki'
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `${context.raw.label || 'Risk'}: (${context.parsed.x}, ${context.parsed.y})`
              }
            }
          }
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Olasılık (1-5)'
            },
            min: 0,
            max: 5
          },
          y: {
            title: {
              display: true,
              text: 'Etki (1-5)'
            },
            min: 0,
            max: 5
          }
        }
      }
    })
  } catch (error) {
    console.error('Chart.js load error:', error)
  }
}

const createResourceChart = async () => {
  await nextTick()
  if (!resourceChart.value) return

  try {
    if (!window.Chart) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
      document.head.appendChild(script)
      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
    }

    resourceChartInstance = destroyChart(resourceChartInstance)

    let chartData

          if (dynamicResourceData.value && dynamicResourceData.value.distribution.length > 0) {
      // Dinamik veri kullan
      const distribution = dynamicResourceData.value.distribution
      chartData = {
        labels: distribution.map(item => item.role),
        datasets: [{
          data: distribution.map(item => item.percentage),
          backgroundColor: distribution.map(item => item.color || 'rgba(59, 130, 246, 0.8)'),
          borderColor: distribution.map(item => item.color || 'rgba(59, 130, 246, 1)'),
          borderWidth: 2
        }]
      }
    } else {
      // Varsayılan veri kullan
      chartData = {
        labels: ['Frontend Developer', 'Backend Developer', 'UI/UX Designer', 'DevOps Engineer', 'QA Engineer'],
        datasets: [{
          data: [30, 35, 15, 10, 10],
          backgroundColor: [
            'rgba(59, 130, 246, 0.8)',
            'rgba(16, 185, 129, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(139, 92, 246, 0.8)',
            'rgba(239, 68, 68, 0.8)'
          ],
          borderColor: [
            'rgba(59, 130, 246, 1)',
            'rgba(16, 185, 129, 1)',
            'rgba(245, 158, 11, 1)',
            'rgba(139, 92, 246, 1)',
            'rgba(239, 68, 68, 1)'
          ],
          borderWidth: 2
        }]
      }
    }

    resourceChartInstance = new window.Chart(resourceChart.value, {
      type: 'doughnut',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Kaynak Dağılımı (%)'
          },
          legend: {
            position: 'bottom'
          }
        }
      }
    })
  } catch (error) {
    console.error('Chart.js load error:', error)
  }
}

const createCostChart = async () => {
  await nextTick()
  if (!costChart.value) return

  try {
    if (!window.Chart) {
      const script = document.createElement('script')
      script.src = 'https://cdn.jsdelivr.net/npm/chart.js'
      document.head.appendChild(script)
      await new Promise((resolve, reject) => {
        script.onload = resolve
        script.onerror = reject
      })
    }

    costChartInstance = destroyChart(costChartInstance)

    let chartData

    if (dynamicCostData.value && dynamicCostData.value.timeline.length > 0) {
      // Dinamik veri kullan
      const timeline = dynamicCostData.value.timeline
      chartData = {
        labels: timeline.map(item => item.month),
        datasets: [{
          label: 'Planlanan Maliyet (₺)',
          data: timeline.map(item => item.planned),
          borderColor: 'rgba(59, 130, 246, 1)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true
        }, {
          label: 'Gerçekleşen Maliyet (₺)',
          data: timeline.map(item => item.actual),
          borderColor: 'rgba(239, 68, 68, 1)',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          tension: 0.4,
          fill: true
        }]
      }
    } else {
      // Varsayılan veri kullan
      chartData = {
        labels: ['Ay 1', 'Ay 2', 'Ay 3', 'Ay 4', 'Ay 5', 'Ay 6'],
        datasets: [{
          label: 'Planlanan Maliyet (₺)',
          data: [50000, 120000, 180000, 220000, 250000, 280000],
          borderColor: 'rgba(59, 130, 246, 1)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true
        }, {
          label: 'Gerçekleşen Maliyet (₺)',
          data: [55000, 125000, 175000, 235000, 260000, 290000],
          borderColor: 'rgba(239, 68, 68, 1)',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          tension: 0.4,
          fill: true
        }]
      }
    }

    costChartInstance = new window.Chart(costChart.value, {
      type: 'line',
      data: chartData,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          title: {
            display: true,
            text: 'Maliyet Tahmini vs Gerçekleşen'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Maliyet (₺)'
            },
            ticks: {
              callback: function(value) {
                return new Intl.NumberFormat('tr-TR', {
                  style: 'currency',
                  currency: 'TRY',
                  minimumFractionDigits: 0
                }).format(value)
              }
            }
          }
        }
      }
    })
  } catch (error) {
    console.error('Chart.js load error:', error)
  }
}

const renderSelectedVisual = async () => {
  switch (selectedVisual.value) {
    case 'orgChart':
      await createOrgChart()
      break
    case 'workflow':
      await createWorkflowChart()
      break
    case 'timeline':
      await createTimelineChart()
      break
    case 'riskAnalysis':
      await createRiskChart()
      break
    case 'resources':
      await createResourceChart()
      break
    case 'cost':
      await createCostChart()
      break
  }
}

// Watch for visual selection changes
watch(selectedVisual, renderSelectedVisual)

// Watch for visual data changes
watch(() => props.visualData, () => {
  if (props.visualData) {
    renderSelectedVisual()
  }
}, { deep: true })

onMounted(async () => {
  await renderSelectedVisual()
})
</script>

<style scoped>
canvas {
  max-height: 400px;
}
</style>
