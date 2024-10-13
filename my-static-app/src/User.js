import React, { useState } from "react";
import "./style.css";

export const User = () => {
  const [name, setName] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [companions, setCompanions] = useState("");
  const [location, setLocation] = useState("");

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
            <div className="text-wrapper-2">Let’s begin.</div>
            <div className="text-wrapper-3">Tell me about yourself...</div>
          </div>
          <div className="overlap-3">
            <div className="form-group">
              <label className="label">Name:</label>
              <input
                className="input-field"
                type="text"
                placeholder="ex: Jane Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="label">Age:</label>
              <input
                className="input-field"
                type="number"
                placeholder="Enter your age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
              />
            </div>

            <div className="form-group">
              <label className="label">Gender:</label>
              <div className="radio-group">
                <label className="radio-label">
                  <input
                    type="radio"
                    name="gender"
                    value="Man"
                    checked={gender === "Man"}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  Man
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="gender"
                    value="Woman"
                    checked={gender === "Woman"}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  Woman
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="gender"
                    value="Other"
                    checked={gender === "Other"}
                    onChange={(e) => setGender(e.target.value)}
                  />
                  Other
                </label>
              </div>
            </div>

            <div className="form-group">
              <label className="label">Who’s traveling with you?</label>
              <div className="radio-group">
                <label className="radio-label">
                  <input
                    type="radio"
                    name="companions"
                    value="Solo"
                    checked={companions === "Solo"}
                    onChange={(e) => setCompanions(e.target.value)}
                  />
                  Solo
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="companions"
                    value="Friends"
                    checked={companions === "Friends"}
                    onChange={(e) => setCompanions(e.target.value)}
                  />
                  Friends
                </label>
                <label className="radio-label">
                  <input
                    type="radio"
                    name="companions"
                    value="Family"
                    checked={companions === "Family"}
                    onChange={(e) => setCompanions(e.target.value)}
                  />
                  Family
                </label>
              </div>
            </div>

            <div className="form-group">
              <label className="label">Location:</label>
              <input
                className="input-field"
                type="text"
                placeholder="Where do you want to travel from?"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};