import React, { useEffect } from "react";
import { useVacationController } from "../controllers/vacationController";

export const VacationList = () => {
  const { vacations, loading, error, fetchVacations } = useVacationController();

  useEffect(() => {
    fetchVacations();
    console.log(vacations)
  }, []);

  if (loading) {
    return <p>Loading vacation...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  // Check if vacations is defined and not null before accessing its fields
  if (!vacations) {
    return <p>No vacation data available.</p>;
  }

  // Assuming vacations is a single object
  return (
    <div className="vacations-list">
      <h1>Saved Vacations</h1>
      <div className="vacation-card">
        <h3>Start: {vacations.flights?.[0]?.first_flight_arrive || "Unknown"} End: {vacations.flights?.[0]?.second_flight_depart || "Unknown"}</h3>
        <p></p>
      </div>
    </div>
  );
};
