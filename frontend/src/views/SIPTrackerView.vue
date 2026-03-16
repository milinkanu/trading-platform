<template>
  <div class="min-h-screen bg-gray-950 text-white font-sans selection:bg-blue-500/30">
    <Navbar />
    
    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-end gap-6">
        <div class="space-y-1">
          <h1 class="text-4xl font-black tracking-tight text-white">SIP & Mutual Fund Tracker</h1>
          <p class="text-gray-500 font-medium">Monitor your systematic investments with live NAV tracking</p>
        </div>
        <button 
          @click="showModal = true"
          class="px-8 py-3 bg-blue-600 hover:bg-blue-500 text-white font-black rounded-xl transition-all shadow-lg active:scale-95 flex items-center space-x-2"
        >
          <span class="text-xl">+</span>
          <span>Add New Fund</span>
        </button>
      </div>

      <!-- Summary Cards -->
      <div v-if="entries.length > 0" class="grid grid-cols-1 md:grid-cols-4 gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
        <div class="bg-gray-900 border border-gray-800 p-5 rounded-2xl">
          <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-1">Total Invested</span>
          <div class="text-2xl font-mono font-bold">₹{{ formatCurrency(stats.totalInvested) }}</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-5 rounded-2xl">
          <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-1">Current Value</span>
          <div class="text-2xl font-mono font-bold">₹{{ formatCurrency(stats.currentValue) }}</div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-5 rounded-2xl">
          <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-1 text-right">Total Gain/Loss</span>
          <div class="text-2xl font-mono font-bold text-right" :class="stats.totalGain >= 0 ? 'text-green-400' : 'text-red-400'">
            {{ stats.totalGain >= 0 ? '+' : '' }}₹{{ formatCurrency(Math.abs(stats.totalGain)) }}
          </div>
        </div>
        <div class="bg-gray-900 border border-gray-800 p-5 rounded-2xl">
          <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest block mb-1 text-right">Overall Returns</span>
          <div class="text-2xl font-mono font-bold text-right" :class="stats.totalReturn >= 0 ? 'text-green-400' : 'text-red-400'">
            {{ stats.totalReturn >= 0 ? '+' : '' }}{{ stats.totalReturn.toFixed(2) }}%
          </div>
        </div>
      </div>

      <!-- Table Section -->
      <div class="bg-gray-900 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl">
        <div class="p-6 border-b border-gray-800 bg-gray-900/50 flex justify-between items-center">
           <h3 class="font-bold">Portfolio Holdings</h3>
           <div v-if="loading" class="text-xs text-blue-500 font-black uppercase tracking-widest animate-pulse">Updating live NAVs...</div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-[10px] font-black text-gray-500 uppercase tracking-widest bg-gray-950/50 border-b border-gray-800">
                <th class="px-6 py-4">Fund Name</th>
                <th class="px-6 py-4 text-right">Scheme Code</th>
                <th class="px-6 py-4 text-right">Current NAV</th>
                <th class="px-6 py-4 text-right">Invested Value</th>
                <th class="px-6 py-4 text-right">Current Value</th>
                <th class="px-6 py-4 text-right">Return P&L</th>
                <th class="px-6 py-4 text-center">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-800">
              <tr v-if="entries.length === 0 && !loading">
                <td colspan="7" class="px-6 py-20 text-center space-y-4">
                   <div class="text-4xl text-gray-700">📜</div>
                   <p class="text-gray-500 font-medium font-italic">No SIP entries found. Start by adding a mutual fund.</p>
                </td>
              </tr>
              <tr v-for="entry in entries" :key="entry.id" class="hover:bg-gray-800/20 transition-colors">
                <td class="px-6 py-5">
                   <div class="font-bold text-white">{{ entry.fund_name }}</div>
                   <div class="text-[10px] text-gray-600 font-mono mt-0.5">Started: {{ entry.start_date }}</div>
                </td>
                <td class="px-6 py-5 text-right font-mono text-xs text-gray-500">{{ entry.scheme_code }}</td>
                <td class="px-6 py-5 text-right">
                   <div class="font-mono text-sm font-bold">₹{{ entry.current_nav?.toFixed(2) || '---' }}</div>
                   <div class="text-[10px] text-gray-600 font-bold uppercase mt-0.5">Live AMFI</div>
                </td>
                <td class="px-6 py-5 text-right">
                   <div class="font-mono text-sm font-bold">₹{{ formatCurrency(entry.invested_value) }}</div>
                   <div class="text-[10px] text-gray-600 mt-0.5">{{ entry.units_held }} Units @ ₹{{ entry.avg_buy_nav }}</div>
                </td>
                <td class="px-6 py-5 text-right font-mono text-sm font-bold">
                   ₹{{ formatCurrency(entry.current_value) }}
                </td>
                <td class="px-6 py-5 text-right">
                   <div :class="entry.gain_loss >= 0 ? 'text-green-500' : 'text-red-500'" class="font-mono text-sm font-black">
                     {{ entry.gain_loss >= 0 ? '+' : '' }}₹{{ formatCurrency(Math.abs(entry.gain_loss)) }}
                   </div>
                   <div :class="entry.gain_pct >= 0 ? 'text-green-600' : 'text-red-600'" class="text-[10px] font-black uppercase">
                     {{ entry.gain_pct >= 0 ? '+' : '' }}{{ entry.gain_pct }}%
                   </div>
                </td>
                <td class="px-6 py-5 text-center">
                   <button @click="deleteEntry(entry)" class="p-2 hover:bg-red-500/20 text-gray-500 hover:text-red-500 rounded-lg transition-all">🗑️</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Modal -->
    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-gray-950/80 backdrop-blur-sm animate-in fade-in duration-300">
       <div class="bg-gray-900 border border-gray-800 rounded-3xl w-full max-w-xl shadow-2xl overflow-hidden">
          <div class="px-8 py-6 border-b border-gray-800 flex justify-between items-center bg-gray-900/50">
             <h3 class="text-xl font-black">Add SIP Investment</h3>
             <button @click="showModal = false" class="text-gray-500 hover:text-white text-2xl">×</button>
          </div>
          
          <div class="p-8 space-y-6">
             <div class="space-y-4">
                <div class="space-y-2">
                   <label class="text-[10px] font-black text-gray-500 uppercase tracking-widest pl-1">Select Fund</label>
                   <select 
                    v-model="newEntry.scheme"
                    class="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-bold"
                   >
                      <option v-for="fund in popularFunds" :key="fund.code" :value="fund">
                        {{ fund.name }}
                      </option>
                   </select>
                </div>

                <div class="grid grid-cols-2 gap-4">
                   <div class="space-y-2">
                      <label class="text-[10px] font-black text-gray-500 uppercase tracking-widest pl-1">Monthly Amount (₹)</label>
                      <input v-model.number="newEntry.monthly_amount" type="number" step="100" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-mono">
                   </div>
                   <div class="space-y-2">
                      <label class="text-[10px] font-black text-gray-500 uppercase tracking-widest pl-1">Start Date</label>
                      <input v-model="newEntry.start_date" type="date" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                   </div>
                </div>

                <div class="grid grid-cols-2 gap-4">
                   <div class="space-y-2">
                      <label class="text-[10px] font-black text-gray-500 uppercase tracking-widest pl-1">Units Held</label>
                      <input v-model.number="newEntry.units_held" type="number" step="0.001" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-mono">
                   </div>
                   <div class="space-y-2">
                      <label class="text-[10px] font-black text-gray-500 uppercase tracking-widest pl-1">Avg Buy NAV (₹)</label>
                      <input v-model.number="newEntry.avg_buy_nav" type="number" step="0.01" class="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all font-mono">
                   </div>
                </div>
             </div>

             <button 
              @click="addSip"
              :disabled="submitting"
              class="w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-black rounded-2xl transition-all shadow-xl shadow-blue-500/20 active:scale-95 text-center mt-4"
             >
                {{ submitting ? 'Adding to Tracker...' : 'Add Investment Record' }}
             </button>
          </div>
       </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import Navbar from '../components/Navbar.vue'
import api from '../api/axios'

const entries = ref([])
const loading = ref(true)
const showModal = ref(false)
const submitting = ref(false)

const popularFunds = [
  { code: '100016', name: 'Axis Bluechip Fund' },
  { code: '119598', name: 'Mirae Asset Large Cap Fund' },
  { code: '120505', name: 'Parag Parikh Flexi Cap Fund' },
  { code: '122639', name: 'Canara Robeco Equity Hybrid' },
  { code: '125354', name: 'SBI Nifty Index Fund' }
]

const newEntry = reactive({
  scheme: popularFunds[0],
  monthly_amount: 5000,
  units_held: 0,
  avg_buy_nav: 0,
  start_date: new Date().toISOString().split('T')[0]
})

const fetchEntries = async () => {
  loading.value = true
  try {
    const response = await api.get('/sip')
    entries.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const addSip = async () => {
  if (!newEntry.monthly_amount || !newEntry.units_held || !newEntry.avg_buy_nav) {
    alert("Please enter monthly amount, units held, and average buy NAV correctly.")
    return
  }
  submitting.value = true
  try {
    await api.post('/sip', {
      fund_name: newEntry.scheme.name,
      scheme_code: newEntry.scheme.code,
      monthly_amount: newEntry.monthly_amount,
      units_held: newEntry.units_held,
      avg_buy_nav: newEntry.avg_buy_nav,
      start_date: newEntry.start_date
    })
    showModal.value = false
    await fetchEntries()
  } catch (err) {
    console.error(err)
    alert("Error adding fund record")
  } finally {
    submitting.value = false
  }
}

const deleteEntry = async (entry) => {
  if (!confirm(`Remove ${entry.fund_name} from your tracker?`)) return
  try {
    await api.delete(`/sip/${entry.id}`)
    await fetchEntries()
  } catch (err) {
    console.error(err)
    alert("Error deleting record")
  }
}

const stats = computed(() => {
  let totalInvested = 0
  let currentValue = 0
  
  entries.value.forEach(e => {
    totalInvested += e.invested_value
    currentValue += e.current_value
  })
  
  const totalGain = currentValue - totalInvested
  const totalReturn = totalInvested > 0 ? (totalGain / totalInvested) * 100 : 0
  
  return { totalInvested, currentValue, totalGain, totalReturn }
})

const formatCurrency = (val) => {
  return new Intl.NumberFormat('en-IN').format(val.toFixed(2))
}

onMounted(fetchEntries)
</script>
