<script setup>
import { useRouter } from 'vue-router';
import store from '@/store';
import {ref} from 'vue';
const router = useRouter();

console.log(store.getters.isDoctor)


</script>

<template>
    <div class="navigation">
        <div class="links">
            <router-link to="/">Home</router-link>
            <router-link to="/query">Query</router-link>
            <router-link to="/visualize">Visualize graph</router-link>
            <router-link to="/tree">Visualize text</router-link>
            <router-link to="/search">Search topics</router-link>
            <router-link to="/medical/history" v-if="store.getters.isAuthenticated && !store.getters.isDoctor">Medical History</router-link>
            <router-link to="/logout" v-if="store.getters.isAuthenticated">Logout</router-link>
        </div>
    </div>
    
</template>

<style scoped>
.test {
  color: white;
  display: flex;
  flex-direction: row;
  gap: 1em;
  width: 30vw;
}

.navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #2C3E50;
    border-bottom: 1px solid #c9c9c9;
}

.navigation .links {
    display: flex;
    margin-left: auto;
    gap: 1em;
    
}
.navigation .links a {
    color: white;
    text-decoration: none;
    font-size: 16px;
}

/* responsiveness */

@media only screen and (max-width: 600px) {

  .left {
    display: flex;
    flex-direction: row;
  }
  .navigation {
    flex-direction: column;
    justify-content: space-around;
    align-items: center;

  }

  .navigation .links {
    flex-direction: row;
    align-items: left;
    margin-left: 20px;
    margin-top: 20px;
  }
}

</style>