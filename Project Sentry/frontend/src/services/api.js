import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data);
      throw new Error(error.response.data.error || 'Server error occurred');
    } else if (error.request) {
      console.error('Network Error:', error.request);
      throw new Error('Network error - please check your connection');
    } else {
      console.error('Error:', error.message);
      throw new Error(error.message);
    }
  }
);

export const apiService = {
  // Health check
  healthCheck: () => api.get('/health'),

  // Projects
  getProjects: () => api.get('/projects'),
  getProject: (projectId) => api.get(`/projects/${projectId}`),

  // File upload
  uploadFile: async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    return api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      },
    });
  },

  // Dashboard
  getDashboard: () => api.get('/dashboard'),

  // Issues
  getIssues: (projectId) => api.get(`/issues/${projectId}`)
};

export default api;