import React from "react";
import {BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./components/HomePage";
import Info from "./components/infopage";
import { User } from "./components/User";
import { Results } from "./components/results";
import { VacationList } from "./components/VacationList";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/infopage" element={<Info />} />
        <Route path="/user" element={<User />} />
        <Route path="/results" element={<Results />} />
        <Route path="/vacationList" element={<VacationList />} />
      </Routes>
    </Router>
  );
};

export default App;