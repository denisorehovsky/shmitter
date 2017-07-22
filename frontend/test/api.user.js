import test from 'ava'
import nock from 'nock'

import User from '../src/api/user'
import { apiURL } from '../src/config'

test('login', t => {
  const token = 'eyJ0eXAiOiJKV'
  const userData = {
    username_or_email: 'testuser@shmitter.com', password: 'password'
  }
  nock(apiURL).post('/auth/login/', userData).reply(200, { token })

  return User.login(userData).then(response => {
    t.is(response.token, token)
  })
})

test('activate', t => {
  const data = {
    uid: 'OQ',
    token: '4n-50689d23'
  }
  nock(apiURL).post('/auth/activate/', data).reply(204)

  return User.activate(data).then(response => {
    t.is(response.status, 204)
  })
})
