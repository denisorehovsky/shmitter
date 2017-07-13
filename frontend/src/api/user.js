import { HTTP } from './common'

export default {
  login (userData, config) {
    return HTTP.post('/auth/login/', userData, config)
  }
}
