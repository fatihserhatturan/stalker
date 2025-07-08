<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-white font-medium">Proje Zaman Çizelgesi</h4>
      <div v-if="data" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
        {{ data.phases.length }} faz planlandı
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

    if (props.data && props.data.phases.length > 0) {
      const phases = props.data.phases
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

    chartInstance = new window.Chart(chartCanvas.value, {
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
