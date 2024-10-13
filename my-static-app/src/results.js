import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./user.css"; // Import user.css for consistent styling
import "./results.css"; // Import results.css for specific styling

export const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { data } = location.state;

  const handleBack = () => {
    navigate("/");
  };

  return (
    <div className="frame">
      <div className="div">
        <div className="overlap-group">
          <div className="overlap">
            <div className="text-wrapper">TravelAI</div>
            <div className="line" aria-label="Line"></div>
            <div className="img" aria-label="Line"></div>
            <div className="line-2" aria-label="Line"></div>
            <button onClick={handleBack} className="big-button back-button">Back</button>
          </div>
          <div className="pexels-michael-block" aria-label="Background image"></div>
          <div className="overlap-2">
            <div className="text-wrapper-2">Trip Details</div>
          </div>
          <div className="overlap-3">
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
                      <li>{hotel.features}</li>
                    )}
                  </ul>
                </div>
              ))}

              <h2>Itinerary</h2>
              {data.itinerary.map((day, index) => (
                <div className="card" key={index}>
                  <h3>Day {index + 1} - {day.date}</h3>
                  {day.activities.map((a, idx) => (
                    <div key={idx}>
                      <p>Activity: {a.activity}</p>
                      <p>Location: {a.location}</p>
                      <p>Dining: {a.dining}</p>
                      <p>Travel: {a.transportation}</p>
                      <p>Wellness: {a["wellness tips"]}</p>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};