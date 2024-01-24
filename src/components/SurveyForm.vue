<script>
import emailjs from 'emailjs-com';

export default {
  data() {
    return {
      showGreeting: true,
      currentQuestionIndex: 0,
      answers: {},
      questions: [
        { id: 'birthday', label: 'Enter your birthday:', type: 'date' },
        {
          id: 'gender',
          label: 'Select your gender:',
          type: 'select',
          placeholder: 'Please select one',
          options: ['Male', 'Female', 'Non-Binary (NB)', 'Choose not to disclose']
        },
        // Add more questions here in the same format
      ],
    };
  },
  methods: {
    beginSurvey() {
      this.showGreeting = false;
    },
    nextQuestion() {
      if (this.currentQuestionIndex === this.questions.length - 1) {
        this.sendEmail();
      } else {
        this.currentQuestionIndex++;
      }
    },
    sendEmail() {
      const templateParams = {
        ...this.answers,
        to_email: 'pentagr4mi@gmail.com',
      };

      emailjs.send('service_kjf34hk', 'template_bmvrb3f', templateParams, 'L_LV-itI8-cF7grnZ')
        .then((response) => {
          this.currentQuestionIndex++;
          console.log('SUCCESS!', response.status, response.text);
        }, (error) => {
          console.log('FAILED...', error);
        });
    }
  }
};
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