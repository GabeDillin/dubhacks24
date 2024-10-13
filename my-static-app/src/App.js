import React from "react";
import {BrowserRouter as Router, Route, Routes } from "react-router-dom";
// import HomePage from "./HomePage";
// import PlannerPage from "./PlannerPage"; 
// import Info from "./info";
import { User } from "./User";
import { Results } from "./results";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<User />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
};

export default App;