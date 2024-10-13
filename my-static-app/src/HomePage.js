import React from "react";
import "./style.css";

const HomePage= () => {
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
          <div className="div">
            <div className="overlap-2">
              <div className="travel-mindfully">
                Travel
                <br />
                mindfully.
              </div>
              <p className="travelai-brings-the">
                <span className="span">
                  TravelAI brings the endless possibility of travel, but in way that prioritizes your{" "}
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
                <div className="text-wrapper-3">Start Planning</div>
              </div>
              <p className="according-to-experts">
                <span className="text-wrapper-4">According to </span>
                <span className="text-wrapper-5">experts,</span>
                <span className="text-wrapper-4"> for optimal </span>
                <span className="text-wrapper-2">wellness</span>
                <span className="text-wrapper-4"> benefits, most people could benefit from taking a dedicated </span>
                <span className="text-wrapper-2">&#34;wellness travel&#34; trip once a year</span>
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