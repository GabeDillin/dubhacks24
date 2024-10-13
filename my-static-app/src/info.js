import React from "react";
import "./info.css"; // Import your CSS file

const Info = () => {
  return (
    <div className="hi">
      {/* The background image is applied through CSS */}
      <a href="#" target="_blank" rel="noopener noreferrer" aria-label="goes to next page"></a>
      <button className="big-button" src="https://apple.com" aria-label="goes to next page">Get Started</button>
    </div>
  );
};

export default Info;