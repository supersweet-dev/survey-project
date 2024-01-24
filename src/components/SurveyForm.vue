<template>
  <form @submit.prevent="sendEmail">
    <label for="birthday">Enter your birthday:</label>
    <input type="date" id="birthday" v-model="birthday" required>
    <button type="submit">Submit</button>
  </form>
</template>

<script>
import emailjs from 'emailjs-com';

export default {
  data() {
    return {
      birthday: ''
    };
  },
  methods: {
    sendEmail() {
      const templateParams = {
        birthday: this.birthday,
        to_email: 'pentagr4mi@gmail.com',
      };

      emailjs.send('service_kjf34hk', 'template_bmvrb3f', templateParams, 'L_LV-itI8-cF7grnZ')
        .then((response) => {
          console.log('SUCCESS!', response.status, response.text);
        }, (error) => {
          console.log('FAILED...', error);
        });
    }
  }
};
</script>
