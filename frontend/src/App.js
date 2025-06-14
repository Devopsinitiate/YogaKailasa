import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Poses from './components/Poses';
import Breathing from './components/Breathing';
import Courses from './components/Courses';
import PaymentSuccess from './components/PaymentSuccess';
import PaymentFailure from './components/PaymentFailure';
import './App.css'; // Keep or modify as needed

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="container mt-3"> {/* Optional: for some basic styling/spacing */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/poses" element={<Poses />} />
          <Route path="/breathing" element={<Breathing />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/payment/success" element={<PaymentSuccess />} />
          <Route path="/payment/failure" element={<PaymentFailure />} />
          {/* Add other routes here, e.g., for login, registration, course details */}
        </Routes>
      </div>
    </div>
  );
}

export default App;
