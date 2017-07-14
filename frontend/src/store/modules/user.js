import {
  AUTHENTICATE,
  DEAUTHENTICATE,
  SET_TOKEN
} from '../mutation-types'

const state = {
  isAuthenticated: false,
  token: null
}

const getters = {
  isAuthenticated: state => state.isAuthenticated,
  isGuest: state => !state.isAuthenticated,
  token: state => state.token
}

const mutations = {
  [AUTHENTICATE] (state) {
    state.isAuthenticated = true
  },
  [DEAUTHENTICATE] (state) {
    state.isAuthenticated = false
    state.token = null
  },
  [SET_TOKEN] (state, { token }) {
    state.token = token
  }
}

const actions = {
  login ({ commit }, payload) {
    commit(SET_TOKEN, payload)
    commit(AUTHENTICATE)
  },
  logout ({ commit }) {
    commit(DEAUTHENTICATE)
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
