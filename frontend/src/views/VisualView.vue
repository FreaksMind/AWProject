<script setup>
import { onBeforeMount, ref } from 'vue'
import axios from "axios";
import cytoscape from "cytoscape";
import avsdf from 'cytoscape-avsdf';

cytoscape.use( avsdf );

axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

let cy = ref(null)

async function test() {
  axios.get("http://127.0.0.1:5000/graph")
      .then(response => {
        cy.value = cytoscape({
          container: document.getElementById("cy"),
          elements: response.data,
          style: [
            {
              selector: "node",
              style: {
                "background-color": "#FFFFFF",
                "color": "gray",
                "label": "data(label)"
              }
            },
            {
              selector: "edge",
              style: {
                "width": 2,
                "line-color": "#AAAAAA",
                "target-arrow-color": "#AAAAAA",
                "target-arrow-shape": "triangle",
                "color": "SlateBlue",
                "label": "data(label)"
              }
            }
          ],
          layout: { name: "avsdf" }
        });
      })
      .catch(error => console.error("Error loading graph:", error));
  }

test();

</script>

<template>
  <div id="container">
    <div id="cy"></div>
  </div>
</template>


<style scoped>

#container {
  width: 100%;
  height: 100%;
}

#cy {
  width: 100%;
  height: 700px;
  color: white;
}
</style>