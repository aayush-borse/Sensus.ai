import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API = axios.create({ baseURL: 'http://localhost:5000/api/v1' });

API.interceptors.request.use(async (cfg) => {
  const token = await SecureStore.getItemAsync('jwt');
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

export default API;
