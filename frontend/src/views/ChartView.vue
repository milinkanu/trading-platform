<template>
  <div class="min-h-screen bg-gray-950 text-white font-sans">
    <Navbar />

    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
      <!-- Header -->
      <div v-if="stockData" class="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 animate-in fade-in slide-in-from-top-4 duration-500">
        <div class="space-y-1">
          <router-link to="/dashboard" class="text-blue-500 text-sm font-bold hover:underline mb-2 block">← Back to Dashboard</router-link>
          <div class="flex items-center space-x-4">
            <h1 class="text-4xl font-black tracking-tighter">{{ stockData.symbol }}</h1>
            <div :class="signalBadgeClass" class="px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest border border-current">
              {{ stockData.signal }}
            </div>
          </div>
          <p class="text-xl text-gray-400 font-medium">{{ stockData.company_name }}</p>
        </div>

        <div class="text-left md:text-right space-y-1">
          <div class="text-4xl font-mono font-bold">${{ stockData.current_price?.toFixed(2) }}</div>
          <div :class="stockData.change_pct >= 0 ? 'text-green-400' : 'text-red-400'" class="text-lg font-bold font-mono">
            {{ stockData.change_pct >= 0 ? '+' : '' }}{{ stockData.change_pct }}%
            <span class="text-xs text-gray-500 ml-2 uppercase tracking-widest">Active Session</span>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div v-if="stockData" class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        <!-- Left: Charts -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Price/SMA Chart -->
          <div class="bg-gray-900 border border-gray-800 rounded-3xl p-6 sm:p-8 space-y-6">
            <div class="flex justify-between items-center">
              <h3 class="text-sm font-black text-gray-500 uppercase tracking-widest">Historical Price & Moving Averages</h3>
              <div class="flex space-x-2">
                <button 
                  @click="toggleSMA('sma20')"
                  :class="showSMA20 ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400'"
                  class="px-3 py-1 text-[10px] font-bold rounded-lg transition-all"
                >
                  SMA 20
                </button>
                <button 
                  @click="toggleSMA('sma50')"
                  :class="showSMA50 ? 'bg-orange-600 text-white' : 'bg-gray-800 text-gray-400'"
                  class="px-3 py-1 text-[10px] font-bold rounded-lg transition-all"
                >
                  SMA 50
                </button>
              </div>
            </div>
            <div class="h-80 w-full">
              <Line :data="priceChartData" :options="priceChartOptions" />
            </div>
          </div>

          <!-- RSI Chart -->
          <div class="bg-gray-900 border border-gray-800 rounded-3xl p-6 sm:p-8 space-y-4">
            <div class="flex justify-between items-center">
              <h3 class="text-sm font-black text-gray-500 uppercase tracking-widest">Relative Strength Index (RSI)</h3>
              <span class="text-xs font-mono font-bold text-gray-400">Curr: {{ stockData.indicators.rsi }}</span>
            </div>
            <div class="h-40 w-full">
              <Line :data="rsiChartData" :options="rsiChartOptions" />
            </div>
          </div>
        </div>

        <!-- Right: Indicators Cards & AI -->
        <div class="space-y-6">
           <!-- Indicator Grid -->
           <div class="grid grid-cols-2 gap-4">
              <div v-for="(val, label) in indicatorDisplay" :key="label" class="bg-gray-900 p-4 border border-gray-800 rounded-2xl">
                <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-1">{{ label }}</span>
                <span class="text-lg font-mono font-bold">{{ typeof val === 'number' ? val.toFixed(2) : val }}</span>
              </div>
           </div>

           <!-- AI Analysis Section -->
           <div class="bg-gray-900 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl relative">
              <div class="bg-gradient-to-r from-blue-600/20 to-purple-600/20 p-6 border-b border-gray-800">
                <div class="flex items-center space-x-3 mb-4">
                  <span class="text-3xl">🤖</span>
                  <h3 class="text-xl font-black tracking-tight">Technical AI View</h3>
                </div>
                <button 
                  @click="fetchAIAnalysis"
                  :disabled="aiLoading"
                  class="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-black rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center space-x-2"
                >
                  <span v-if="aiLoading">Analyzing with Claude...</span>
                  <span v-else>{{ aiResult ? 'Refresh Analysis' : 'Get Deep Analysis' }}</span>
                </button>
              </div>

              <div class="p-6 min-h-[100px] flex flex-col justify-center">
                 <div v-if="aiLoading" class="space-y-4 animate-pulse">
                    <div class="h-4 bg-gray-800 rounded w-full"></div>
                    <div class="h-4 bg-gray-800 rounded w-5/6"></div>
                    <div class="h-12 bg-gray-800 rounded w-full mt-4"></div>
                 </div>

                 <div v-else-if="aiResult" class="space-y-6">
                    <div class="flex justify-between items-center">
                       <span :class="signalBadgeClass" class="px-4 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border border-current">
                         {{ aiResult.recommendation }}
                       </span>
                       <div class="flex items-center space-x-2">
                          <span class="text-[10px] font-black text-gray-500 uppercase">Confidence</span>
                          <span :class="confidenceClass" class="text-[10px] font-bold uppercase tracking-widest">{{ aiResult.confidence }}</span>
                       </div>
                    </div>

                    <p class="text-sm leading-relaxed text-gray-300 font-medium italic">"{{ aiResult.summary }}"</p>

                    <div class="p-4 bg-red-500/10 border border-red-500/20 rounded-2xl">
                      <span class="text-[10px] font-black text-red-400 uppercase tracking-widest block mb-1">Key Risk</span>
                      <p class="text-xs text-red-300/80">{{ aiResult.key_risk }}</p>
                    </div>

                    <div class="p-4 bg-blue-500/10 border border-blue-500/20 rounded-2xl">
                      <span class="text-[10px] font-black text-blue-400 uppercase tracking-widest block mb-1">Price Levels</span>
                      <p class="text-xs text-blue-300/80">{{ aiResult.target_note }}</p>
                    </div>
                 </div>

                 <div v-else class="text-center py-6">
                    <p class="text-sm text-gray-500 font-medium italic">Click above to generate a technical summary of {{ stockData.symbol }} using Claude AI.</p>
                 </div>
              </div>
           </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import api from '../api/axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const route = useRoute()
const stockData = ref(null)
const loading = ref(true)
const aiLoading = ref(false)
const aiResult = ref(null)

const showSMA20 = ref(true)
const showSMA50 = ref(true)

const toggleSMA = (type) => {
  if (type === 'sma20') showSMA20.value = !showSMA20.value
  else showSMA50.value = !showSMA50.value
}

const fetchStock = async () => {
  try {
    const symbol = route.params.symbol
    const response = await api.get(`/stock/${symbol}`)
    stockData.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const fetchAIAnalysis = async () => {
  aiLoading.value = true
  try {
    const symbol = route.params.symbol
    const response = await api.get(`/stock/${symbol}/ai`)
    aiResult.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    aiLoading.value = false
  }
}

onMounted(fetchStock)

// === Computed ===

const indicatorDisplay = computed(() => {
  if (!stockData.value) return {}
  return {
    'RSI (14)': stockData.value.indicators.rsi,
    'MACD': stockData.value.indicators.macd,
    'BB Upper': stockData.value.indicators.bb_upper,
    'BB Lower': stockData.value.indicators.bb_lower,
    'SMA 20': stockData.value.indicators.sma20,
    'SMA 50': stockData.value.indicators.sma50
  }
})

const signalBadgeClass = computed(() => {
  const s = aiResult.value?.recommendation || stockData.value?.signal
  if (s === 'BUY') return 'bg-green-500/20 text-green-400 border-green-500/30'
  if (s === 'SELL') return 'bg-red-500/20 text-red-400 border-red-500/30'
  return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
})

const confidenceClass = computed(() => {
  const c = aiResult.value?.confidence
  if (c === 'High') return 'text-green-400'
  if (c === 'Low') return 'text-red-400'
  return 'text-yellow-400'
})

const priceChartData = computed(() => {
  if (!stockData.value) return null
  const d = stockData.value.chart_data

  const datasets = [
    {
      label: 'Price',
      data: d.map(x => x.close),
      borderColor: '#22c55e',
      borderWidth: 2.5,
      pointRadius: 0,
       backgroundColor: (context) => {
          const chart = context.chart;
          const {ctx, chartArea} = chart;
          if (!chartArea) return null;
          const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
          gradient.addColorStop(0, 'rgba(34, 197, 94, 0.15)');
          gradient.addColorStop(1, 'rgba(34, 197, 94, 0)');
          return gradient;
        },
      fill: true,
      tension: 0.2
    }
  ]

  if (showSMA20.value) {
    datasets.push({
      label: 'SMA 20',
      data: d.map(x => x.sma20),
      borderColor: '#3b82f6',
      borderWidth: 1.5,
      borderDash: [5, 5],
      pointRadius: 0,
      fill: false,
      tension: 0.1
    })
  }

  if (showSMA50.value) {
    datasets.push({
      label: 'SMA 50',
      data: d.map(x => x.sma50),
      borderColor: '#f97316',
      borderWidth: 1.5,
      borderDash: [5, 5],
      pointRadius: 0,
      fill: false,
      tension: 0.1
    })
  }

  return {
    labels: d.map(x => x.date),
    datasets
  }
})

const rsiChartData = computed(() => {
  if (!stockData.value) return null
  const d = stockData.value.chart_data
  return {
    labels: d.map(x => x.date),
    datasets: [{
      label: 'RSI',
      data: d.map(x => x.rsi),
      borderColor: '#a78bfa',
      borderWidth: 2,
      pointRadius: 0,
      tension: 0.2,
      fill: false
    }]
  }
})

// === Chart Options ===

const priceChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      padding: 10,
      cornerRadius: 8,
      displayColors: true,
      borderColor: '#374151',
      borderWidth: 1
    }
  },
  scales: {
    x: { grid: { display: false }, ticks: { display: false } },
    y: { grid: { color: '#1f2937' }, ticks: { color: '#6b7280', font: { size: 10 } } }
  }
}

const rsiChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: { 
    legend: { display: false },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      padding: 8,
      displayColors: false
    }
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#6b7280', font: { size: 10 } } },
    y: { 
      min: 0, max: 100, 
      grid: { 
        color: (context) => (context.tick.value === 30 || context.tick.value === 70) ? 'rgba(239, 68, 68, 0.4)' : '#1f2937',
        lineWidth: (context) => (context.tick.value === 30 || context.tick.value === 70) ? 2 : 1
      },
      ticks: { stepSize: 30, color: '#6b7280' }
    }
  }
}
</script>
