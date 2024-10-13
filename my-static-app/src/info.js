import React from "react";
import "./info.css"; // Import your CSS file

const Info = () => {
  return (
    <div className="hi">
      {/* The background image is applied through CSS */}
      <a href="https://www.apple.com" target="_blank" rel="noopener noreferrer"></a>
      <button className="big-button" src="https://apple.com">Get Started</button>
    </div>
  );
};

export default Info;