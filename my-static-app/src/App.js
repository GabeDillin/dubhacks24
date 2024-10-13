// App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import Info from './Info';
import User from './User';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/info" element={<Info />} />
        <Route path="/user" element={<User />} />
      </Routes>
    </Router>
  );
}

export default App;
