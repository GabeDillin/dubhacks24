import axios from 'axios';

// Set the base URL for the API
const BASE_URL = 'http://localhost:8080/api/v1'; // Replace with your API base URL
const VacationService = {
  // GET: Fetch all objects
  getAll: async () => {
    return axios.get(`${BASE_URL}/vacations`);
  },

  // GET by ID: Fetch object by ID
  getById: async (id) => {
    return axios.get(`${BASE_URL}/vacations/${id}`);
  },

  // POST: Create new object
  create: async (data) => {
    return axios.post(`${BASE_URL}/vacations`, data);
  },

  // DELETE: Delete object by ID
  delete: async (id) => {
    return axios.delete(`${BASE_URL}/vacations/${id}`);
  }
};

export default VacationService;
