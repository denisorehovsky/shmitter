import test from 'ava'

import user from '../src/store/modules/user'
import * as types from '../src/store/mutation-types'

// Mutations

test('AUTHENTICATE', t => {
  const AUTHENTICATE = user.mutations[types.AUTHENTICATE]
  const state = {
    isAuthenticated: false
  }
  AUTHENTICATE(state)

  t.true(state.isAuthenticated)
})

test('DEAUTHENTICATE', t => {
  const DEAUTHENTICATE = user.mutations[types.DEAUTHENTICATE]
  const state = {
    isAuthenticated: false,
    token: 'eyJ0eXAiOiJKV'
  }
  DEAUTHENTICATE(state)

  t.false(state.isAuthenticated)
  t.is(state.token, null)
})

test('SET_TOKEN', t => {
  const SET_TOKEN = user.mutations[types.SET_TOKEN]
  const state = {
    token: null
  }
  const payload = {
    token: 'eyJ0eXAiOiJKV'
  }
  SET_TOKEN(state, payload)

  t.is(state.token, 'eyJ0eXAiOiJKV')
})
