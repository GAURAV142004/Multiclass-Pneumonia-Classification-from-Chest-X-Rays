/**
 * API Service
 * Handles all HTTP requests to the backend
 */
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

// ============= Authentication API =============

export const authAPI = {
  signup: async (email, password, fullName) => {
    const response = await api.post("/api/v1/auth/signup", {
      email,
      password,
      full_name: fullName,
    });
    return response.data;
  },

  login: async (email, password) => {
    const response = await api.post("/api/v1/auth/login", {
      email,
      password,
    });
    return response.data;
  },

  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },
};

// ============= User API =============

export const userAPI = {
  getProfile: async () => {
    const response = await api.get("/api/v1/users/me");
    return response.data;
  },

  updateProfile: async (fullName) => {
    const response = await api.put("/api/v1/users/me", {
      full_name: fullName,
    });
    return response.data;
  },

  changePassword: async (currentPassword, newPassword) => {
    const response = await api.post("/api/v1/users/change-password", {
      current_password: currentPassword,
      new_password: newPassword,
    });
    return response.data;
  },

  getScanHistory: async (limit = 10) => {
    const response = await api.get(`/api/v1/users/history?limit=${limit}`);
    return response.data;
  },
};

// ============= Inference API =============

export const inferenceAPI = {
  predictPneumonia: async (file, onUploadProgressOrRunStage2, runStage2 = false) => {
    // Handle polymorphic parameters (backward compatibility)
    let onUploadProgress = null;
    let shouldRunStage2 = false;

    if (typeof onUploadProgressOrRunStage2 === 'boolean') {
      shouldRunStage2 = onUploadProgressOrRunStage2;
    } else if (typeof onUploadProgressOrRunStage2 === 'function') {
      onUploadProgress = onUploadProgressOrRunStage2;
      shouldRunStage2 = runStage2;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await api.post(
      `/api/v1/inference/predict?run_stage2=${shouldRunStage2}`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress,
      }
    );
    return response.data;
  },

  getModelsStatus: async () => {
    const response = await api.get("/api/v1/inference/models/status");
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get("/api/v1/inference/health");
    return response.data;
  },
};

export default api;
