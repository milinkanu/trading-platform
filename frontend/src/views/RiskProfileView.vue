<template>
  <div class="min-h-screen bg-gray-950 text-white font-sans selection:bg-blue-500/30">
    <Navbar />
    
    <main class="max-w-3xl mx-auto p-6 sm:p-12 space-y-8">
      <!-- Intro Section -->
      <div v-if="step === 0" class="text-center space-y-6 py-12 animate-in fade-in zoom-in duration-500">
        <div class="space-y-4">
          <h1 class="text-4xl sm:text-5xl font-black tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-500">
            Know Your Investor Profile
          </h1>
          <p class="text-gray-400 text-lg max-w-lg mx-auto leading-relaxed">
            Every great portfolio starts with a clear plan. Answer 5 quick questions to discover your personalized risk profile and ideal asset allocation.
          </p>
        </div>
        <button 
          @click="step = 1"
          class="px-12 py-4 bg-blue-600 hover:bg-blue-500 text-white font-black rounded-2xl transition-all shadow-xl shadow-blue-500/20 active:scale-95 text-lg"
        >
          Start Assessment
        </button>
      </div>

      <!-- Quiz Step -->
      <div v-else-if="step <= 5" class="bg-gray-900 border border-gray-800 rounded-3xl p-8 sm:p-10 space-y-8 relative overflow-hidden shadow-2xl animate-in slide-in-from-right duration-300">
        <!-- Progress Bar -->
        <div class="flex justify-between items-center mb-4">
           <div class="flex space-x-2">
             <div 
               v-for="i in 5" :key="i"
               :class="i <= step ? 'bg-blue-500' : 'bg-gray-800'"
               class="w-3 h-3 rounded-full transition-colors duration-500"
             ></div>
           </div>
           <span class="text-xs font-black text-gray-500 uppercase tracking-widest">Question {{ step }} of 5</span>
        </div>

        <div class="space-y-2">
          <h2 class="text-2xl font-black tracking-tight leading-tight">
            {{ currentQuestion.text }}
          </h2>
          <p class="text-gray-500 text-sm font-medium">Select the option that best describes you.</p>
        </div>

        <div class="grid grid-cols-1 gap-4">
          <button 
            v-for="(label, key) in currentQuestion.options" :key="key"
            @click="answers[currentQuestion.id] = key"
            :class="answers[currentQuestion.id] === key 
              ? 'border-blue-500 bg-blue-500/10 text-blue-400' 
              : 'border-gray-800 bg-gray-950/50 text-gray-400 hover:border-gray-600'"
            class="w-full text-left px-6 py-5 rounded-2xl border transition-all flex items-center justify-between group"
          >
            <span class="font-bold text-lg">{{ label }}</span>
            <div 
              :class="answers[currentQuestion.id] === key ? 'bg-blue-500 scale-125' : 'bg-gray-800'"
              class="w-5 h-5 rounded-full flex items-center justify-center transition-all"
            >
               <div v-if="answers[currentQuestion.id] === key" class="w-1.5 h-1.5 bg-white rounded-full"></div>
            </div>
          </button>
        </div>

        <div class="flex justify-between items-center pt-4">
          <button 
            @click="step--"
            class="text-gray-500 font-bold hover:text-white transition-colors flex items-center space-x-2"
          >
            <span>←</span> <span>Back</span>
          </button>
          <button 
            @click="nextStep"
            :disabled="!answers[currentQuestion.id]"
            class="px-8 py-3 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold rounded-xl transition-all shadow-lg active:scale-95"
          >
            {{ step === 5 ? 'See Results' : 'Next Step →' }}
          </button>
        </div>
      </div>

      <!-- Result Card -->
      <div v-else-if="result" class="bg-gray-900 border border-gray-800 rounded-3xl p-8 sm:p-12 space-y-10 shadow-2xl animate-in zoom-in duration-500">
        <div class="text-center space-y-4">
           <div class="inline-block px-4 py-1.5 rounded-full bg-blue-500/10 text-blue-400 text-xs font-black uppercase tracking-widest border border-blue-500/20 mb-2">
             Your Results are Ready
           </div>
           <h2 class="text-4xl font-black tracking-tighter">{{ result.type }}</h2>
           <p class="text-gray-400 font-medium max-w-sm mx-auto">{{ result.description }}</p>
           <div class="text-sm font-mono text-gray-500 font-bold">Total Score: {{ result.score }} / 14</div>
        </div>

        <div class="space-y-6">
           <h3 class="text-xs font-black text-gray-500 uppercase tracking-widest text-center">Recommended Asset Allocation</h3>
           <div class="grid grid-cols-1 gap-6">
              <div v-for="(val, asset) in result.allocation" :key="asset" class="space-y-2">
                <div class="flex justify-between items-center text-sm font-bold uppercase tracking-wider">
                   <span class="text-gray-400">{{ asset }}</span>
                   <span class="text-white">{{ val }}%</span>
                </div>
                <div class="h-3 w-full bg-gray-950 rounded-full overflow-hidden border border-gray-800">
                   <div 
                    :class="assetColor(asset)"
                    :style="{ width: val + '%' }" 
                    class="h-full rounded-full transition-all duration-1000 delay-300"
                   ></div>
                </div>
              </div>
           </div>
        </div>

        <div class="pt-8 border-t border-gray-800 flex flex-col sm:flex-row gap-4">
           <router-link to="/dashboard" class="flex-1 px-8 py-4 bg-blue-600 hover:bg-blue-500 text-white font-black rounded-2xl transition-all shadow-xl shadow-blue-500/20 text-center">
             Go to Dashboard
           </router-link>
           <button @click="resetQuiz" class="px-8 py-4 bg-gray-800 hover:bg-gray-700 text-gray-300 font-black rounded-2xl transition-all text-center">
             Retake Quiz
           </button>
        </div>
        
        <p v-if="result.saved" class="text-center text-xs font-bold text-green-500 uppercase tracking-widest">✓ Profile saved to your account</p>
      </div>

      <!-- Loading State -->
      <div v-if="submitting" class="text-center py-20 space-y-6 animate-pulse">
        <div class="text-5xl">🧠</div>
        <p class="text-gray-400 font-black uppercase tracking-widest">Calculating your optimal strategy...</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Navbar from '../components/Navbar.vue'
import api from '../api/axios'

const step = ref(0)
const answers = ref({})
const result = ref(null)
const submitting = ref(false)

const questions = [
  {
    id: 'q1',
    text: 'What is your primary investment goal?',
    options: {
      'wealth_creation': 'Wealth Creation (Long term appreciation)',
      'regular_income': 'Regular Income (Moderate growth)',
      'capital_protection': 'Capital Protection (Safety first)'
    }
  },
  {
    id: 'q2',
    text: 'What is your planned investment horizon?',
    options: {
      'less_1yr': 'Less than 1 year',
      '1_to_3yr': '1 to 3 years',
      '3_plus_yr': '3+ years'
    }
  },
  {
    id: 'q3',
    text: 'How comfortable are you with market fluctuations?',
    options: {
      'uncomfortable': 'Very Uncomfortable (Sell if price drops)',
      'somewhat_ok': 'Somewhat Comfortable (Hold through cycles)',
      'very_comfortable': 'Very Comfortable (Buy more on dips)'
    }
  },
  {
    id: 'q4',
    text: 'What is your existing market experience?',
    options: {
      'none': 'No Experience (New investor)',
      'some_mf_sip': 'Moderate (Currently in SIP/MF)',
      'active_trader': 'Expert (Active stock trader)'
    }
  },
  {
    id: 'q5',
    text: 'How much of your savings will be deployed in the market?',
    options: {
      'less_25': 'Less than 25%',
      '25_to_50': '25% to 50%',
      'more_50': 'More than 50%'
    }
  }
]

const currentQuestion = computed(() => questions[step.value - 1])

const nextStep = async () => {
  if (step.value < 5) {
    step.value++
  } else {
    submitProfile()
  }
}

const submitProfile = async () => {
  submitting.value = true
  step.value = 6 // Loading state
  try {
    const response = await api.post('/onboarding/profile', { answers: answers.value })
    result.value = response.data
    // If logic above updated DB, we might want to refresh authStore in a real app
    // But for now, just show result.
  } catch (err) {
    console.error(err)
    alert("Error calculating profile. Please try again.")
    step.value = 5
  } finally {
    submitting.value = false
  }
}

const resetQuiz = () => {
  step.value = 0
  answers.value = {}
  result.value = null
}

const assetColor = (asset) => {
  switch (asset) {
    case 'equity': return 'bg-blue-500'
    case 'mf': return 'bg-indigo-500'
    case 'gold': return 'bg-yellow-500'
    case 'debt': return 'bg-gray-400'
    default: return 'bg-blue-500'
  }
}
</script>
