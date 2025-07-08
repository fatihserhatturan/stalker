<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <h4 class="text-white font-medium">Maliyet Tahmini</h4>
      <div v-if="data" class="text-xs text-emerald-400 bg-emerald-400/10 px-2 py-1 rounded">
        {{ data.timeline.length }} aylık projeksiyon
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

    if (props.data && props.data.timeline.length > 0) {
      const timeline = props.data.timeline
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

    chartInstance = new window.Chart(chartCanvas.value, {
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
