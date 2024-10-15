import React, { useEffect, useState } from "react";
import { useVacationController } from "../controllers/vacationController";// Assuming the controller is set up for fetching

export const VacationList = () => {
  const { vacations, fetchVacations } = useVacationController(); // Assuming fetchObjects retrieves the saved vacations
  const [vacationsDisplay, setDisplayVacations] = useState([]);

  useEffect(() => {
    // Fetch all saved vacations on component mount
    fetchVacations().then(setDisplayVacations).catch(console.error);
  }, [fetchVacations]);

  return (
    <div className="vacations-list">
      <h1>All Saved Vacations</h1>
      <div className="vacations-container">
        {vacationsDisplay.map((vacationsDisplay, index) => (
          <div className="vacation-card" key={index}>
            <h3>Destination: {vacationsDisplay.flights[0].first_flight_arrive}</h3>
            <p>Date: {vacationsDisplay.itinerary[0].date}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
