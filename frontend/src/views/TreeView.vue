<template>
  <div class="container">
    
    <div>
      <h2>Classes</h2>
      <ul>
        <li v-for="cls in classes" :key="cls" @click="fetchIndividuals(cls)">
          {{ cls }}
        </li>
      </ul>
    </div>

    <div v-if="selectedClass">
      <h2>Individuals of {{ selectedClass }}</h2>
      <ul>
        <p v-if="individuals.length == 0">No entries found :(</p>
        <li v-for="ind in individuals" :key="ind" @click="fetchProperties(ind)">
          {{ ind }}
        </li>
      </ul>
    </div>

    <div v-if="selectedIndividual">
      <h2>Properties of {{ selectedIndividual }}</h2>
      <ul>
        <p v-if="individuals.length == 0">No entries found :(</p>
        <li v-for="(value, prop) in properties" :key="prop">
          <strong>{{ prop }}:</strong> {{ value }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      classes: [],
      individuals: [],
      properties: {},
      selectedClass: null,
      selectedIndividual: null,
    };
  },
  methods: {
    async fetchClasses() {
      const response = await axios.get("http://127.0.0.1:5000/classes");
      this.classes = response.data;
    },
    async fetchIndividuals(cls) {
      this.selectedClass = cls;
      this.selectedIndividual = null;
      this.properties = {};
      const response = await axios.get("http://127.0.0.1:5000/individuals", {
        params: { class_uri: cls },
      });
      this.individuals = response.data;
    },
    async fetchProperties(ind) {
      this.selectedIndividual = ind;
      const response = await axios.get("http://127.0.0.1:5000/properties", {
        params: { individual_uri: ind },
      });
      this.properties = response.data;
      console.log(this.properties);
    },
  },
  mounted() {
    this.fetchClasses();
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  text-align: left;
}
h1, h2, p {
  text-align: center;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  padding: 8px;
  cursor: pointer;
  border-bottom: 1px solid #ddd;
}
li:hover {
  background-color: transparent;
}
</style>