<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from 'axios'

let queryResults = ref([]);
let error = ref();
let query = ref("");
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

async function executeQuery() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/list_repos", { 
      params: {
      topic: query.value
    }
  });
        const data = response.data;
        console.log(data.results)
        queryResults.value = data;
        if (data.error) {
          error = data.error;
          return;
        }

      } catch (err) {
        error = "Failed to fetch data.";
        console.error(err);
      }
    }

</script>
<template>
  <div class="container">
    <h2>Repository search</h2>
    <textarea v-model="query" placeholder="Enter a topic here"></textarea>
    <button @click="executeQuery">Run</button>
    <table v-if="queryResults.length">
      <thead>
        <tr>
          <th v-for="(value, index) in queryResults[0]" :key="index">{{ value }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(result, index) in queryResults" :key="index">
          <td v-for="(value, key) in result" :key="key">{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<style scoped>
  .container {
  max-width: 800px;
  margin: auto;
}
textarea {
  width: 100%;
  height: 100px;
  color: white;
  border: 1px solid #ccc;
}
button {
  margin-top: 10px;
  margin-bottom: 20px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.error {
  color: red;
}
h2 {
  margin-bottom: 10px;
  margin-top: 10px;
}
</style>