import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const API_URL = '/api'; // Adjust if your Django API is on a different base URL

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('authToken'));

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
      // Optionally, fetch user profile here if token exists to validate it
      // and get user details. For now, we'll assume the token is valid if it exists.
      // A placeholder user object could be set or fetched from localStorage too.
      // For simplicity, we won't fetch user profile on load here, but it's good practice.
      // setUser({ token }); // Or some user info if stored
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_URL}/login/`, { username, password });
      setToken(response.data.token);
      setUser({ username: response.data.username, email: response.data.email, id: response.data.user_id }); // Adjust based on your login response
      localStorage.setItem('authToken', response.data.token);
      // Store minimal user info if needed, or fetch full profile
      localStorage.setItem('authUser', JSON.stringify({ username: response.data.username, email: response.data.email, id: response.data.user_id }));
      axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
      return response.data;
    } catch (error) {
      console.error('Login failed', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : new Error('Login failed');
    }
  };

  const register = async (username, email, password) => {
    try {
      const response = await axios.post(`${API_URL}/register/`, { username, email, password });
      // Registration now also returns a token and user info
      setToken(response.data.token);
      setUser({ username: response.data.username, email: response.data.email, id: response.data.user_id });
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('authUser', JSON.stringify({ username: response.data.username, email: response.data.email, id: response.data.user_id }));
      axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
      return response.data;
    } catch (error) {
      console.error('Registration failed', error.response ? error.response.data : error.message);
      throw error.response ? error.response.data : new Error('Registration failed');
    }
  };

  const logout = async () => {
    try {
      if (token) {
        await axios.post(`${API_URL}/logout/`, {}, {
          headers: { 'Authorization': `Token ${token}` }
        });
      }
    } catch (error) {
      // Even if logout API call fails, clear client-side auth state
      console.error('Logout API call failed, logging out client-side anyway.', error.response ? error.response.data : error.message);
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem('authToken');
      localStorage.removeItem('authUser');
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  // On initial load, try to get user from localStorage if token exists
  useEffect(() => {
    const storedToken = localStorage.getItem('authToken');
    const storedUser = localStorage.getItem('authUser');
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
      axios.defaults.headers.common['Authorization'] = `Token ${storedToken}`;
    }
  }, []);


  const value = {
    user,
    token,
    isAuthenticated: !!token, // Or more robustly: user && token
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
