import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

let accessToken = localStorage.getItem('token');

const axiosInstance = axios.create({
  baseURL: `${API_BASE}/api`,
  withCredentials: true, // to send cookies like refreshToken
  headers: {
    Authorization: accessToken ? `Bearer ${accessToken}` : undefined
  }
});

// Automatically attach the latest token
axiosInstance.interceptors.request.use(
  (config) => {
    const newToken = localStorage.getItem('token');
    if (newToken) config.headers.Authorization = `Bearer ${newToken}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle 401 & refresh token flow
axiosInstance.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes('/auth/refresh-token')
    ) {
      originalRequest._retry = true;
      try {
        const res = await axios.post(`${API_BASE}/api/auth/refresh-token`, {}, {
          withCredentials: true
        });

        const newAccessToken = res.data.accessToken;
        localStorage.setItem('token', newAccessToken);

        axiosInstance.defaults.headers.Authorization = `Bearer ${newAccessToken}`;
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        return axiosInstance(originalRequest);
      } catch (refreshErr) {
        console.error('Refresh token failed:', refreshErr);
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/login'; // force logout
        return Promise.reject(refreshErr);
      }
    }

    return Promise.reject(error);
  }
);

export default axiosInstance;
