import React from "react";
import { useNavigate } from "react-router-dom"; // Import useNavigate from react-router-dom
import "./info.css"; // Import the corresponding CSS file

const Info = () => {
  const navigate = useNavigate(); // Initialize the navigate function

  return (
    <div className="hi">
      {/* Anchor tag with proper href and accessibility */}
      <a href="https://www.apple.com" target="_blank" rel="noopener noreferrer">Visit Apple</a>
      {/* Button to navigate to the User component */}
      <button className="big-button" onClick={() => navigate("/user")}>
        Get Started
      </button>
    </div>
  );
};

export default Info;