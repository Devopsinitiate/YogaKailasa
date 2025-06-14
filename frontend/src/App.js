import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './components/Home';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage'; // Import ProfilePage
import ProtectedRoute from './components/ProtectedRoute';
import Footer from './components/Footer'; // Import Footer
import Poses from './components/Poses';
import Breathing from './components/Breathing';
import Courses from './components/Courses';
import PaymentSuccess from './components/PaymentSuccess';
import PaymentFailure from './components/PaymentFailure';
import './App.css'; // Keep or modify as needed

function App() {
  return (
    <AuthProvider>
      <div className="App">
        <Navbar />
        <div className="container mt-3"> {/* Optional: for some basic styling/spacing */}
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />

            {/* Publicly viewable */}
            <Route path="/poses" element={<Poses />} />
            <Route path="/breathing" element={<Breathing />} />

            {/* Protected Routes */}
            {/* Courses list can be public, but buying/accessing specific course content would be protected */}
            {/* For now, let's make viewing courses list public, but actions inside (like buy) will check auth. */}
            {/* If we want to protect the whole /courses route:
            <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
            */}
            <Route path="/courses" element={<Courses />} />
            {/* Payment related pages are typically accessed after an action, protection might depend on flow */}
            {/* PaymentSuccess might be okay to be public as it verifies based on ref from URL */}
            <Route path="/payment/success" element={<PaymentSuccess />} />
            <Route path="/payment/failure" element={<PaymentFailure />} />

            {/* Example of a fully protected route:
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}

export default App;
