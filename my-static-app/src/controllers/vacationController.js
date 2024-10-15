// objectController.js
import { useState, useEffect } from 'react';
import VacationService from '../services/vacationService';

export const useVacationController = () => {
  const [vacations, setVacations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all objects
  const fetchVacations = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await VacationService.getAll();
      setVacations(response.data);
    } catch (err) {
      setError('Failed to fetch vacations');
    } finally {
      setLoading(false);
    }
  };

  // Fetch a specific object by ID
  const fetchVacationById = async (id) => {
    setLoading(true);
    setError(null);
    try {
      const response = await VacationService.getById(id);
      return response.data;
    } catch (err) {
      setError(`Failed to fetch vacation with ID: ${id}`);
    } finally {
      setLoading(false);
    }
  };

  // Create a new object
  const createVacation = async (newVacation) => {
    setLoading(true);
    setError(null);
    try {
      const response = await VacationService.create(newVacation);
      // Optionally refresh the list of objects
      await fetchVacations();
      return response.data;
    } catch (err) {
      setError('Failed to create Vacation');
    } finally {
      setLoading(false);
    }
  };

  // Delete an object
  const deleteVacation = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await VacationService.delete(id);
      // Optionally refresh the list of objects
      await fetchVacations();
    } catch (err) {
      setError(`Failed to delete vacation with ID: ${id}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVacations();
  }, []);

  return {
    vacations,
    loading,
    error,
    fetchVacations,
    fetchVacationById,
    createVacation,
    deleteVacation,
  };
};
