import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import axios from 'axios'; // Assuming axios is used in AuthContext and configured with token

function ProfilePage() {
  const { user, token } = useAuth(); // Get user from AuthContext if already populated
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      if (!token) {
        setError('Not authenticated. Please login.');
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        setError('');
        // Axios instance should have Authorization header set by AuthContext
        const response = await axios.get('/api/profile/');
        setProfile(response.data);
      } catch (err) {
        console.error("Error fetching profile:", err);
        setError(err.response?.data?.detail || err.message || 'Failed to fetch profile.');
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [token]); // Re-fetch if token changes (e.g. after login)

  if (loading) {
    return <div className="container mt-3 loading-message"><p>Loading profile...</p></div>;
  }

  if (error) {
    return <div className="container mt-3 alert alert-danger error-message">{error}</div>;
  }

  if (!profile) {
    return <div className="container mt-3 text-center"><p>No profile data found.</p></div>;
  }

  // User data from AuthContext might be more up-to-date for username/email
  // Profile data from API for other specific profile fields
  const displayUser = profile.user || user;

  return (
    <div className="container mt-3">
      <h1 className="page-title">User Profile</h1>
      {displayUser && (
        <div className="item-card mb-3"> {/* Using item-card for consistency */}
            <h3 className="text-primary">Account Information</h3>
            <p><strong>Username:</strong> {displayUser.username}</p>
            <p><strong>Email:</strong> {displayUser.email}</p>
            {/* Add other display fields from profile.user if needed */}
        </div>
      )}

      {/* Placeholder for other profile fields if UserProfile model had them e.g. bio */}
      {/* {profile.bio && <div className="item-card mb-3"><h3>Bio</h3><p>{profile.bio}</p></div>} */}

      {/* Enrolled Courses will be a separate component */}
      <EnrolledCoursesList />
    </div>
  );
}

// Remove forward declaration, import actual component
import EnrolledCoursesList from '../components/EnrolledCoursesList';

export default ProfilePage;
