import { HTTP } from './common'

export default {
  login (userData, config) {
    return HTTP.post('/auth/login/', userData, config)
      .then(response => {
        return response.data
      })
  },
  activate (data, config) {
    return HTTP.post('/auth/activate/', data, config)
  }
}
