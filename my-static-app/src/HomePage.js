// HomePage.js
import React from "react";
import { useNavigate } from 'react-router-dom';
import "./HomePage.css";

const HomePage = () => {
  const navigate = useNavigate();

  const handleStartPlanning = () => {
    navigate('/info');
  };

  return (
    <div className="frame">
      <div className="overlap-group-wrapper">
        <div className="overlap-group">
          <div className="overlap">
            <div className="text-wrapper">Wellness Trip Planner</div>
            <img className="line" alt="Line" src="/Line-19.png" />
            <img className="img" alt="Line" src="/Line-19.png" />
            <img className="line-2" alt="Line" src="/Line-19.png" />
          </div>
          <div className="content">
            <div className="overlap-2">
              <div className="travel-mindfully">
                Travel
                <br />
                mindfully.
              </div>
              <p className="travelai-brings-the">
                <span className="span">
                  TravelAI brings the endless possibility of travel, but in a way that prioritizes your{" "}
                </span>
                <span className="text-wrapper-2">
                  well-being.
                  <br />
                  <br />
                </span>
              </p>
            </div>
            <div className="overlap-3">
              <div className="div-wrapper">
                {/* Changed from div to button for accessibility */}
                <button className="start-planning-button" onClick={handleStartPlanning}>
                  Start Planning
                </button>
              </div>
              <p className="according-to-experts">
                <span className="text-wrapper-4">According to </span>
                <span className="text-wrapper-5">experts,</span>
                <span className="text-wrapper-4"> for optimal </span>
                <span className="text-wrapper-2">wellness</span>
                <span className="text-wrapper-4"> benefits, most people could benefit from taking a dedicated </span>
                <span className="text-wrapper-2">“wellness travel” trip once a year</span>
                <span className="text-wrapper-4"> to fully reset and recharge both mentally and physically</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;