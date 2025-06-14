import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }
    setError('');
    try {
      await register(username, email, password);
      alert('Registration successful! Please login.'); // Or redirect to login/home
      navigate('/login');
    } catch (err) {
      // Process DRF validation errors (likely a dictionary)
      if (typeof err === 'object' && err !== null) {
        let errorMessages = [];
        for (const key in err) {
          if (Array.isArray(err[key])) {
            errorMessages.push(`${key}: ${err[key].join(' ')}`);
          } else {
            errorMessages.push(String(err[key]));
          }
        }
        setError(errorMessages.join(' '));
      } else {
        setError('Failed to register. Please try again.');
      }
      console.error("Register page error:", err);
    }
  };

  return (
    <div className="auth-card">
      <h2 className="card-title text-center">Register</h2>
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
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    // className="form-control" // Global styles will apply
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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
                <div className="form-group mb-3">
                  <label htmlFor="confirmPassword">Confirm Password</label>
                  <input
                    type="password"
                    // className="form-control" // Global styles will apply
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
                <button type="submit" className="btn btn-primary w-100">Register</button>
              </form>
              <p className="mt-3 text-center">
                Already have an account? <Link to="/login">Login here</Link>
              </p>
    </div>
  );
}

export default RegisterPage;
