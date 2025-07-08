<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-white font-medium">Risk Analizi</h4>
      <div v-if="data" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
        {{ data.risks.length }} risk tespit edildi
      </div>
    </div>
    <canvas ref="chartCanvas" class="w-full h-96 bg-white rounded-lg"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'

const props = defineProps({
  data: Object
})

const emit = defineEmits(['chart-ready'])

const chartCanvas = ref(null)
let chartInstance = null

const createChart = async () => {
  if (!chartCanvas.value) return

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

    if (chartInstance) {
      chartInstance.destroy()
    }

    let chartData

    if (props.data && props.data.risks.length > 0) {
      const risks = props.data.risks
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

    chartInstance = new window.Chart(chartCanvas.value, {
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

    emit('chart-ready', chartCanvas.value)
  } catch (error) {
    console.error('Chart.js load error:', error)
  }
}

onMounted(createChart)
watch(() => props.data, createChart, { deep: true })

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.destroy()
  }
})
</script>
