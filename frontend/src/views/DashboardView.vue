<template>
  <div class="min-h-screen bg-gray-950 text-white font-sans selection:bg-blue-500/30">
    <Navbar />
    
    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
      <!-- Search & Popular -->
      <header class="space-y-6">
        <div class="relative max-w-2xl group">
          <div class="absolute inset-y-0 left-4 flex items-center pointer-events-none">
            <span class="text-xl">🔍</span>
          </div>
          <input 
            v-model="symbolInput"
            @keyup.enter="searchStock"
            type="text" 
            placeholder="Search stock symbol (e.g., AAPL, RELIANCE.NS)..."
            class="w-full bg-gray-900 border border-gray-800 rounded-2xl py-4 pl-12 pr-32 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all text-lg font-mono placeholder:text-gray-600"
          />
          <button 
            @click="searchStock"
            :disabled="loading"
            class="absolute right-2 inset-y-2 px-6 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold rounded-xl transition-all shadow-lg active:scale-95"
          >
            {{ loading ? '...' : 'Analyze' }}
          </button>
        </div>

        <div class="flex items-center space-x-3 overflow-x-auto pb-2 scrollbar-hide">
          <span class="text-xs font-black text-gray-500 uppercase tracking-widest whitespace-nowrap">Popular:</span>
          <button 
            v-for="symbol in popularSymbols" 
            :key="symbol"
            @click="selectSymbol(symbol)"
            class="px-4 py-1.5 bg-gray-900 border border-gray-800 hover:border-blue-500 rounded-full text-xs font-bold text-gray-300 transition-all hover:-translate-y-0.5"
          >
            {{ symbol }}
          </button>
        </div>
      </header>

      <!-- Error State -->
      <div v-if="error" class="p-6 bg-red-500/10 border border-red-500/30 rounded-2xl flex items-center space-x-4 animate-in fade-in slide-in-from-bottom-2">
        <span class="text-2xl">⚠️</span>
        <div>
          <h4 class="font-bold text-red-400">Analysis Failed</h4>
          <p class="text-sm text-red-300/80">{{ error }} — Try AAPL, TSLA or RELIANCE.NS</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && !stockData" class="space-y-8 animate-pulse">
        <div class="h-64 bg-gray-900/50 rounded-3xl border border-gray-800"></div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="h-24 bg-gray-900/50 rounded-2xl border border-gray-800"></div>
        </div>
      </div>

      <!-- Dashboard Grid -->
      <div v-if="stockData" class="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8 animate-in fade-in duration-500">
        
        <!-- Left Column: Price & Chart -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-gray-900 rounded-3xl border border-gray-800 p-6 sm:p-8 space-y-6 relative overflow-hidden group">
            <!-- Background Glow -->
            <div class="absolute -top-24 -right-24 w-64 h-64 bg-blue-500/5 blur-3xl rounded-full group-hover:bg-blue-500/10 transition-colors duration-700"></div>
            
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative z-10">
              <div>
                <h2 class="text-3xl font-black tracking-tighter">{{ stockData.symbol }}</h2>
                <p class="text-gray-400 font-medium">{{ stockData.company_name }}</p>
              </div>
              <div class="text-right">
                <div class="text-3xl font-mono font-bold">${{ stockData.current_price?.toFixed(2) }}</div>
                <div :class="stockData.change_pct >= 0 ? 'text-green-400' : 'text-red-400'" class="font-bold font-mono">
                  {{ stockData.change_pct >= 0 ? '+' : '' }}{{ stockData.change_pct }}%
                  <span class="ml-1 text-xs uppercase tracking-widest text-gray-500 font-bold">Today</span>
                </div>
              </div>
            </div>

            <!-- Main Chart Area -->
             <div class="h-80 w-full relative z-10 pt-4">
              <Line v-if="chartDataComputed" :data="chartDataComputed" :options="chartOptions" />
            </div>

            <div class="flex flex-col sm:flex-row justify-between items-center pt-6 gap-4 border-t border-gray-800 relative z-10">
               <div :class="signalBadgeClass" class="px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest border border-current shadow-lg shadow-current/5">
                {{ stockData.signal }}
              </div>
              <p class="text-sm font-medium text-gray-400 text-center sm:text-left">{{ stockData.signal_reason }}</p>
              <router-link 
                :to="`/chart/${stockData.symbol}`" 
                class="px-6 py-2 bg-gray-800 hover:bg-gray-700 text-sm font-bold rounded-xl transition-all self-stretch sm:self-auto text-center"
              >
                Full Analysis →
              </router-link>
            </div>
          </div>
        </div>

        <!-- Right Column: Indicators -->
        <div class="lg:col-span-1 flex flex-col gap-6">
          <h4 class="text-xs font-black text-gray-500 uppercase tracking-widest px-2">Market Sentiment</h4>
          
          <div class="grid grid-cols-1 gap-4">
            <!-- RSI Card -->
            <div class="bg-gray-900 p-5 rounded-2xl border border-gray-800 hover:border-blue-500/50 transition-colors group">
              <div class="flex justify-between items-center mb-1">
                <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">RSI (14)</span>
                <span class="text-[10px] font-black group-hover:text-blue-500 transition-colors">OSCILLATOR</span>
              </div>
              <div class="flex items-baseline space-x-2">
                <div class="text-2xl font-mono font-bold">{{ stockData.indicators.rsi }}</div>
                <span :class="rsiStatusClass" class="text-[10px] font-black uppercase tracking-widest">{{ rsiStatusText }}</span>
              </div>
            </div>

            <!-- MACD Card -->
            <div class="bg-gray-900 p-5 rounded-2xl border border-gray-800 flex justify-between items-center">
              <div>
                 <span class="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1">MACD Base</span>
                 <div class="text-xl font-mono font-bold" :class="stockData.indicators.macd >= 0 ? 'text-green-400' : 'text-red-400'">{{ stockData.indicators.macd?.toFixed(3) }}</div>
              </div>
               <div>
                 <span class="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-1 text-right">Signal</span>
                 <div class="text-xl font-mono font-bold text-right">{{ stockData.indicators.macd_signal?.toFixed(3) }}</div>
              </div>
            </div>

            <!-- BB Bands Card -->
             <div class="bg-gray-900 p-5 rounded-2xl border border-gray-800 space-y-3">
               <span class="text-xs font-bold text-gray-500 uppercase tracking-wider">Bollinger Bands</span>
               <div class="flex justify-between items-center">
                 <div class="text-center">
                    <span class="text-[10px] text-gray-600 block mb-1">LOWER</span>
                    <span class="font-mono text-sm font-bold">${{ stockData.indicators.bb_lower?.toFixed(2) }}</span>
                 </div>
                 <div class="h-8 w-px bg-gray-800"></div>
                  <div class="text-center">
                    <span class="text-[10px] text-gray-600 block mb-1 uppercase">Upper</span>
                    <span class="font-mono text-sm font-bold">${{ stockData.indicators.bb_upper?.toFixed(2) }}</span>
                 </div>
               </div>
            </div>

             <!-- SMA Card -->
            <div class="bg-gray-900 p-5 rounded-2xl border border-gray-800">
               <span class="text-xs font-bold text-gray-500 uppercase tracking-wider block mb-3">Moving Averages</span>
               <div class="space-y-2">
                 <div class="flex justify-between items-center">
                   <div class="flex items-center space-x-2">
                     <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                     <span class="text-xs font-bold text-gray-400">SMA 20</span>
                   </div>
                   <span class="font-mono text-sm font-bold italic">${{ stockData.indicators.sma20?.toFixed(2) }}</span>
                 </div>
                  <div class="flex justify-between items-center">
                   <div class="flex items-center space-x-2">
                     <span class="w-2 h-2 rounded-full bg-orange-500"></span>
                     <span class="text-xs font-bold text-gray-400">SMA 50</span>
                   </div>
                   <span class="font-mono text-sm font-bold italic">${{ stockData.indicators.sma50?.toFixed(2) }}</span>
                 </div>
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
import Navbar from '../components/Navbar.vue'
import api from '../api/axios'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const symbolInput = ref('')
const loading = ref(false)
const error = ref('')
const stockData = ref(null)
const popularSymbols = ['AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT', 'RELIANCE.NS', 'TCS.NS', 'INFY.NS']

const searchStock = async () => {
  if (!symbolInput.value) return
  loading.value = true
  error.value = ''
  try {
    const response = await api.get(`/stock/${symbolInput.value.toUpperCase()}`)
    stockData.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to fetch stock data'
    stockData.value = null
  } finally {
    loading.value = false
  }
}

const selectSymbol = (s) => {
  symbolInput.value = s
  searchStock()
}

onMounted(() => {
  symbolInput.value = 'AAPL'
  searchStock()
})

// === Computed Logic ===

const signalBadgeClass = computed(() => {
  if (!stockData.value) return ''
  switch (stockData.value.signal) {
    case 'BUY': return 'bg-green-500/20 text-green-400 border-green-500/30'
    case 'SELL': return 'bg-red-500/20 text-red-400 border-red-500/30'
    default: return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30'
  }
})

const rsiStatusClass = computed(() => {
  const rsi = stockData.value?.indicators.rsi
  if (rsi < 30) return 'text-green-400'
  if (rsi > 70) return 'text-red-400'
  return 'text-gray-500'
})

const rsiStatusText = computed(() => {
  const rsi = stockData.value?.indicators.rsi
  if (rsi < 30) return 'Oversold'
  if (rsi > 70) return 'Overbought'
  return 'Neutral'
})

const chartDataComputed = computed(() => {
  if (!stockData.value) return null
  
  // Last 30 days for dashboard
  const limitedData = stockData.value.chart_data.slice(-30)
  
  return {
    labels: limitedData.map(d => d.date.split('-').slice(1).join('/')),
    datasets: [
      {
        label: 'Price',
        data: limitedData.map(d => d.close),
        borderColor: '#22c55e',
        backgroundColor: (context) => {
          const chart = context.chart;
          const {ctx, chartArea} = chart;
          if (!chartArea) return null;
          const gradient = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
          gradient.addColorStop(0, 'rgba(34, 197, 94, 0.2)');
          gradient.addColorStop(1, 'rgba(34, 197, 94, 0)');
          return gradient;
        },
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
        tension: 0.2
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: { display: false },
    tooltip: {
      enabled: true,
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      titleColor: '#fff',
      bodyColor: '#fff',
      borderColor: '#374151',
      borderWidth: 1,
      padding: 10,
      displayColors: true,
    }
  },
  scales: {
    x: { grid: { display: false }, ticks: { color: '#6b7280', font: { size: 10 } } },
    y: { grid: { color: '#1f2937' }, ticks: { color: '#6b7280', font: { size: 10 } } }
  }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
