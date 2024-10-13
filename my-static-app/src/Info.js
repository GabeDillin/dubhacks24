// Info.js
import React from "react";
import "./info.css"; // Import the corresponding CSS file

const Info = () => {
  return (
    <div className="hi">
      {/* Anchor tag with proper href and accessibility */}
      <a href="https://www.apple.com" target="_blank" rel="noopener noreferrer">Visit Apple</a>
      {/* Single button that will trigger navigation or action */}
      <button className="big-button" onClick={() => window.location.href="https://apple.com"}>
        Get Started
      </button>
    </div>
  );
};

export default Info;
