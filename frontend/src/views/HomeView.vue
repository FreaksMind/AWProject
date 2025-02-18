<script setup>
import axios from "axios"
import AuthForm from "../components/AuthForm.vue"
import LoadingCircle from "@/components/LoadingCircle.vue"
import BubbleButton from "../components/BubbleButton.vue"
import { ref } from "vue"
import { download_ontology, generate_ontology } from '@/api'
import store from "@/store"

const medicData = ref({
    city: "",
    specialization: ""
  }),
  loading = ref(false),
  error = ref(false),
  step = ref(0),
  salut = ref([]);
  const snackbar = ref(false);
  var timeout = 2000;
  var text = ref("teste");

async function populate_onto(){
  await generate_ontology()
}

async function download(){
    const data = await download_ontology()

    const blob = new Blob([data])
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = "Ontology.owl"
    link.click()
}

</script>

<template>
  <LoadingCircle class="loading-component " :loading="loading" />
  <div v-if="error">error</div>
  <div class="app" v-if="!loading && !store.getters.isAuthenticated">
    <div class="buttons-container">
      <router-link to="/query" custom v-slot="{ navigate }"><BubbleButton @click="navigate" role="link" label="Query the Ontology"></BubbleButton></router-link>
      <router-link to="/visualize" custom v-slot="{ navigate }"><BubbleButton @click="navigate" role="link" label="Visualize the Ontology - Graph"></BubbleButton></router-link>
      <router-link to="/tree" custom v-slot="{ navigate }"><BubbleButton @click="navigate" role="link" label="Visualize the Ontology - Text"></BubbleButton></router-link>
      <router-link to="/search" custom v-slot="{ navigate }"><BubbleButton @click="navigate" role="link" label="Search topics"></BubbleButton></router-link>
      <BubbleButton label="Generate Ontology" @click="populate_onto"></BubbleButton>
      <BubbleButton label="Download Ontology" @click="download"></BubbleButton>
    </div>
  </div>
  <div class="forms">
    <div class="login-form" v-if="!loading && store.getters.isAuthenticated && step === 0">
      <AuthForm class="form" @submit="test" />
    </div>
  </div>
</template>


<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.app {
  text-align: center;
}

.logo-container {
  margin-bottom: 30px;
}

.logo {
  width: 150px; /* Set logo size as per requirement */
}

.buttons-container {
  display: flex;
  gap: 20px; /* Add space between buttons */
  justify-content: center; /* Center the buttons horizontally */
  margin-top: 500px;
}

.loading-component{
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;

}

.login-form {
  border: 1px solid white;
  border-radius: 20px;
  background-color: rgba(6, 140, 100, 0.1);

}

.forms{
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  align-content: center;
  height: 100%;
}


.form {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 100px;
  margin: 0 auto;
}

/* responsiveness */
@media only screen and (max-width: 1130px) {
  .forms{
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
  }

  .form {
    margin-bottom: 60px;
  }

}
</style>