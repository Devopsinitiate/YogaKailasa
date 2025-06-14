import React, { useState } from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from?.pathname || "/";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await login(username, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.detail || err.message || 'Failed to login. Please check your credentials.');
      console.error("Login page error:", err);
    }
  };

  return (
    // Container class added by App.js main content wrapper, or keep it if pages manage their own top container
    // For auth-card, we want it centered.
    <div className="auth-card">
      <h2 className="card-title text-center">Login</h2>
      {error && <div className="alert alert-danger error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group mb-3">
                  <label htmlFor="username">Username</label>
                  <input
                    type="text"
                    // className="form-control" // Global styles will apply
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group mb-3">
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    // className="form-control" // Global styles will apply
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">Login</button>
              </form>
              <p className="mt-3 text-center">
                Don't have an account? <Link to="/register">Register here</Link>
              </p>
    </div>
  );
}

export default LoginPage;
