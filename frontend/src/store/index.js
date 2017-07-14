import Vue from 'vue'
import Vuex from 'vuex'

import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'

import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user
  },
  plugins: [
    createPersistedState({
      paths: ['user.isAuthenticated', 'user.token'],
      getState: (key) => Cookies.getJSON(key),
      setState: (key, state) => Cookies.set(key, state, { expires: 1 })
    })
  ]
})
