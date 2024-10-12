// src/HomePage.js
import React from 'react';
import './HomePage.css'; // Import the CSS file for homepage styling

const HomePage = () => {
  return (
    <div className="homepage-container">
      <header className="homepage-header">
        <h1>Welcome to My React App</h1>
        <p>This is the front page of your application. Explore and enjoy!</p>
        <button className="cta-button">Get Started</button>
      </header>
    </div>
  );
};

export default HomePage;