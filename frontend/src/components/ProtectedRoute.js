import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// This component can be used to protect routes that require authentication.
// It can also be extended to handle role-based authorization if needed.

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, token } = useAuth(); // Using token as a proxy for loading state if user object is fetched async
  const location = useLocation();

  // A more robust check might involve a loading state from useAuth if user profile is fetched
  // For example: if (isLoading) return <LoadingSpinner />;

  // Check if we have a token. If not, definitely not authenticated.
  // If isAuthenticated is false but we have a token, it might mean user info is still loading
  // or token is invalid. For simplicity, we rely on isAuthenticated.
  if (!isAuthenticated) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
};

export default ProtectedRoute;
