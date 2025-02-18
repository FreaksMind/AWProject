import Vuex from 'vuex'
import {ref} from 'vue'

import { login, register, get_user_details} from '@/api'
import { isValidJwt} from '@/utils'
import createPersistedState from "vuex-persistedstate";

const state = {
    user: {},
    jwt: '',
    user_details: {}
  }

let message = ref('')


  const actions = {
    // asynchronous operations
    logout (context) {
        context.commit('logoutUser')    
    },
    async login (context, userData) {
      console.log('logiigiiiinn')
      await login(userData)
        .then(response => {
          message.value = 'Logged in!'
            context.commit('setJwtToken', { jwt: response.data })
            context.commit('setUserData', { userData })
            context.dispatch('retrieveUserDetails', userData.email)
        })
        .catch(error => {
          console.log('Error Authenticating: ', error.response.data['message'])
          message.value = error.response.data['message']
        })
        return message.value
    },
    async register (context, userData) {
      await register(userData)
        .then(() => {
            //context.commit('setUserData', { userData })
            //context.dispatch('login', userData)
        })
        .catch(error => {
          console.log('Error Registering: ', error)
          message.value = error.response.data['message']
          //EventBus.emit('failedRegistering: ', error)
        })
        return message.value
    },
    retrieveUserDetails(context, email){
      return get_user_details({'email': email})
      .then((response) => {
          context.commit('setUserDetails', response)
      })
    }
  }
  const mutations = {
    // isolated data mutations
    setUserData (state, payload) {
      console.log('setUserData payload = ', payload)
      state.user = payload.userData
    },
    setJwtToken (state, payload) {
      console.log('setJwtToken payload = ', payload)
      localStorage.token = payload.jwt.token
      state.jwt = payload.jwt
    },
    logoutUser (state){
        console.log('logout user')
        localStorage.token = ''
        state.jwt = ''
        state.user = {}
        state.user_details = {}
    },
    setUserDetails (state , payload){
      state.user_details = payload
    }
  }
  
  const getters = {
    // reusable data accessors
    isAuthenticated (state) {
      return isValidJwt(state.jwt.token)
    },
    getUserEmail(state){
      if(!getters.isAuthenticated(state)) { return null; }
      return state.user['email'];
    },
    isDoctor(state) {
      console.log(state)
      if(!getters.isAuthenticated(state)) { return null; }
      return state.user_details['8']
    },
    getUserId(state) {
      if(!getters.isAuthenticated(state)) { return null; }
      return state.user_details['0']
    },
    getPhone_number(state) {
      if(!getters.isAuthenticated(state)) { return null; }
      return state.user_details['3']
    },
    getEmail(state) {
      if(!getters.isAuthenticated(state)) { return null; }
      return state.user_details['4']
    }
  }
  
  const store = new Vuex.Store({
    state,
    actions,
    mutations,
    getters,
    plugins: [createPersistedState({
      paths: ['user', 'jwt', 'user_details']
    })]
  })
  
export default store