import axios from 'axios'
import { apiURL } from '../config'

export const HTTP = axios.create({
  baseURL: apiURL
})
