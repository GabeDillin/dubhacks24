// HomePage.js
import React from "react";
import { useNavigate } from 'react-router-dom';
import "./HomePage.css";


const HomePage = () => {
  const navigate = useNavigate();
  return (
    <div className="frame1">
      <button className="big-button" onClick={() => navigate("/infopage")} aria-label="goes to next page">
        Get Started
      </button>
    </div>
  );
};

export default HomePage;