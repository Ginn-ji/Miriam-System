import axios from 'axios';

// Read from Vercel environment variables, fallback to localhost for dev
const BACKEND_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
const API = `${BACKEND_URL}/api`;

const apiClient = axios.create({
  baseURL: API,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export { apiClient, API };
export default apiClient;