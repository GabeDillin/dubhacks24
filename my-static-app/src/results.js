import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./results.css";

export const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { data } = location.state;

  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="results-container">
      <h1>Trip Details</h1>
      <button onClick={handleBack} className="back-button">Back</button>
      <div className="cards-container">
        <h2>Flights</h2>
        {data.flights.map((flight, index) => (
          <div className="card" key={index}>
            <h3>Flight {index + 1}</h3>
            <p>Airline: {flight.airline}</p>
            <p>Flight Number (Departure): {flight.first_flight_number}</p>
            <p>Departure: {flight.first_flight_depart}</p>
            <p>Arrival: {flight.first_flight_arrive}</p>
            <p>Flight Number (Return): {flight.second_flight_number}</p>
            <p>Departure: {flight.second_flight_depart}</p>
            <p>Arrival: {flight.second_flight_arrive}</p>
            <p>Price: {flight.price}</p>
            <p>Emissions: {flight.emissions_data.estimated_emissions}</p>
          </div>
        ))}

        <h2>Accommodation</h2>
        {data.accommodation.map((hotel, index) => (
          <div className="card" key={index}>
            <h3>{hotel.name}</h3>
            <p>Location: {hotel.location}</p>
            <p>Price per Night: {hotel.price_per_night}</p>
            <p>Total Price for Week: {hotel.total_price_for_week}</p>
            <p>Features:</p>
            <ul>
              {Array.isArray(hotel.features) ? (
                hotel.features.map((feature, idx) => (
                  <li key={idx}>{feature}</li>
                ))
              ) : (
                <li>No features available</li>
              )}
            </ul>
          </div>
        ))}

        <h2>Itinerary</h2>
        {data.itinerary.map((day, index) => (
          <div className="card" key={index}>
            <h3>Day {index + 1} - {day.date}</h3>
            {day.activities.map((activity, idx) => (
              <div key={idx}>
                <p>Activity: {activity["activity name"]}</p>
                <p>Location: {activity.location}</p>
                <p>Dining: {activity.dining}</p>
                <p>Travel: {activity.travel}</p>
                <p>Wellness: {activity.wellness}</p>
              </div>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};