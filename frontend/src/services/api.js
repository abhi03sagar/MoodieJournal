import axiosInstance from './axiosInstance';

/**
 * Logs in the user with provided credentials.
 * @param {string} username 
 * @param {string} password 
 * @returns {Promise<AxiosResponse>}
 */
export const login = (username, password) =>
  axiosInstance.post('/auth/login', { username, password });

/**
 * Registers a new user and logs them in.
 * @param {string} username 
 * @param {string} password 
 * @returns {Promise<AxiosResponse>}
 */
export const register = (username, password) =>
  axiosInstance.post('/auth/register', { username, password });

/**
 * Fetches all diary entries for the authenticated user.
 * @returns {Promise<AxiosResponse>}
 */
export const getEntries = () =>
  axiosInstance.get('/entries');

/**
 * Creates a new diary entry.
 * @param {string} text 
 * @returns {Promise<AxiosResponse>}
 */
export const createEntry = (text) =>
  axiosInstance.post('/entries', { text });

/**
 * Deletes a diary entry by ID.
 * @param {string} id 
 * @returns {Promise<AxiosResponse>}
 */
export const deleteEntry = (id) =>
  axiosInstance.delete(`/entries/${id}`);

/**
 * Downloads a diary entry as a PDF.
 * @param {string} id 
 * @returns {Promise<AxiosResponse>}
 */
export const downloadPDF = (id) =>
  axiosInstance.get(`/entries/${id}/download`, {
    responseType: 'blob'
  });

/**
 * Edits a diary entry by ID.
 * @param {string} id 
 * @param {string} newText 
 * @returns {Promise<AxiosResponse>}
 */
export const editEntry = (id, newText) =>
  axiosInstance.put(`/entries/${id}`, { text: newText });
