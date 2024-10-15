import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./user.css";

export const User = () => {
  const [formData, setFormData] = useState({
    flightFrom: "",
    flightTo: "",
    flightDate: "",
    flightReturnDate: "",
    budget: "",
    numAdults: ""
  });
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/trip-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      console.log("Data:", data);
      setLoading(false);
      navigate("/results", { state: { data } });
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
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
          </div>
          <div className="pexels-michael-block" aria-label="Background image"></div>
          <div className="overlap-2">
            {loading ? (
              <div className="text-wrapper-2"> Your trip is being planned...</div>
            ) : (
              <>
                <div className="text-wrapper-2">Let’s begin.</div>
                <div className="text-wrapper-3">Tell me about your trip...</div>
              </>
            )}
          </div>
          <div className="overlap-3">
            {loading ? (
              <div className="loading-spinner"></div>
            ) : (
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label className="label">Airport Leaving From:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="text"
                      name="flightFrom"
                      placeholder="ex: LAX"
                      value={formData.flightFrom}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Airport Arriving At:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="text"
                      name="flightTo"
                      placeholder="ex: JFK"
                      value={formData.flightTo}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Flight Departure Date:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="date"
                      name="flightDate"
                      value={formData.flightDate}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Flight Return Date:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="date"
                      name="flightReturnDate"
                      value={formData.flightReturnDate}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Budget:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="number"
                      name="budget"
                      placeholder="Enter your budget"
                      value={formData.budget}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="label">Number of Adults:</label>
                  <div className="input-wrapper">
                    <input
                      className="input-field"
                      type="number"
                      name="numAdults"
                      placeholder="Enter number of adults"
                      value={formData.numAdults}
                      onChange={handleChange}
                      required
                    />
                  </div>
                </div>

                <button type="submit" className="big-button" aria-label="submit form">
                  Get Started
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};