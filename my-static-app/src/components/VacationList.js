import React, { useEffect, useState } from "react";
import { useVacationController } from "../controllers/vacationController"; // Assuming the controller is set up for fetching

export const VacationList = () => {
  const { vacations, fetchVacations } = useVacationController(); // Assuming fetchObjects retrieves the saved vacations
  const [vacationsData, setVacationsData] = useState([]); // State to store the fetched vacations

  useEffect(() => {
    // Fetch all saved vacations on component mount
    fetchVacations()
      .then((data) => {
        setVacationsData(data); // Store the fetched vacations in state
        console.log("Fetched Vacations: ", data); // Log the fetched vacations
      })
      .catch(console.error);
  }, [fetchVacations]);

  return (
    <div className="vacations-list">
      <h1>All Saved Vacations</h1>
      <div className="vacations-container">
        {vacationsData?.map((vacation, index) => (
          <div className="vacation-card" key={index}>
            <h3>Destination: {vacation.flights[0].first_flight_arrive}</h3>
            <p>Date: {vacation.itinerary[0].date}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
