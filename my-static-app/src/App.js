import React from "react";
import {BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./HomePage";
import Info from "./infopage";
import { User } from "./User";
import { Results } from "./results";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/infopage" element={<Info />} />
        <Route path="/user" element={<User />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
};

export default App;