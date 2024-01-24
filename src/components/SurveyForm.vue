<script setup>
// supabaseClient.js
import { createClient } from '@supabase/supabase-js';
import { onMounted, ref } from 'vue';

const supabaseUrl = 'https://nppobcantxohrbjqjfni.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5wcG9iY2FudHhvaHJianFqZm5pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDYxMDQwNjEsImV4cCI6MjAyMTY4MDA2MX0.dUp7XxmLfOJ5JEKKcd0xSMkrl0iArsKyT2wVfsZVJaw';
const supabase = createClient(supabaseUrl, supabaseKey);
const answers = ref({});
const showGreeting = ref(true)
const currentQuestionIndex = ref(0)
const questions =[
  { id: 'date_of_birth', label: 'Enter your birthday:', type: 'date' },
  {
    id: 'gender',
    label: 'Select your gender:',
    type: 'select',
    placeholder: 'Please select one',
    options: ['Male', 'Female', 'Non-Binary (NB)', 'Choose not to disclose']
  },
]
const beginSurvey = () => {
  showGreeting.value = false
}
const nextQuestion = () => {
  if (currentQuestionIndex.value === questions.length - 1) {
    sendResponse()
  } else {
    currentQuestionIndex.value++;
  }
}
const sendResponse = async () => {
  console.log(answers.value)
  const { data, error } = await supabase
    .from('responses')
    .insert([answers.value]);

  if (error) {
    console.error('Error submitting to Supabase:', error);
  } else {
    console.log('Submitted to Supabase:', data);
    // Add any post-submission logic here
  }
}
async function getRandomQuestionCombination() {
  const { data, error } = await supabase
    .rpc('random_question_combination').single(); // Using a stored procedure

  if (error) {
    console.error('Error fetching random question combination:', error);
    return null;
  }

  return data;
}
onMounted(async ()=>{
  const randomQ = await getRandomQuestionCombination()
  console.log(randomQ)
  await supabase
  .from('question_combinations')
  .update({counter: randomQ.counter + 1})
  .eq('id', randomQ.id)
})

</script>
<template>
  <div class="max-w-md mx-auto mt-10 p-6 rounded-lg shadow-md bg-white">
    <div v-if="showGreeting" class="text-center">
      <h2 class="text-lg font-semibold text-gray-800">Welcome to Our Survey</h2>
      <button @click="beginSurvey"
        class="mt-4 py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75">
        Begin Survey
      </button>
    </div>

    <form v-else-if="currentQuestionIndex < questions.length" @submit.prevent="nextQuestion" class="flex flex-col gap-4">
      <div v-for="(question, index) in questions" :key="index">
        <div v-if="index === currentQuestionIndex">
          <label :for="question.id" class="block text-sm font-bold text-gray-700">{{ question.label }}</label>
          <input v-if="question.type === 'date'" :type="question.type" :id="question.id" v-model="answers[question.id]"
            required
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
          <select v-else :id="question.id" v-model="answers[question.id]" required
            class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
            <option disabled value="">{{ question.placeholder }}</option>
            <option v-for="option in question.options" :key="option" :value="option">{{ option }}</option>
          </select>
        </div>
      </div>
      <button type="submit"
        class="py-2 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-lg shadow-md focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-opacity-75">
        {{ currentQuestionIndex === questions.length - 1 ? 'Submit' : 'Next' }}
      </button>
    </form>

    <div v-else class="text-center">
      <h2 class="text-lg font-semibold text-gray-800">Thanks! Your response has been submitted.</h2>
    </div>
  </div>
</template>