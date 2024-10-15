import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate for routing
import "./info.css"; // Import the corresponding CSS file

const Info = () => {
  const navigate = useNavigate(); // Initialize navigate function

  return (
    <div className="frame2">
      <button className="big-button" onClick={() => navigate("/user")} aria-label="goes to next page">
        Get Started
      </button>
    </div>
  );
};

export default Info;