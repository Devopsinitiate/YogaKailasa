import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Assuming axios is configured with token by AuthContext
import { Link } from 'react-router-dom';

function EnrolledCoursesList() {
  const [enrolledCourses, setEnrolledCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchEnrolledCourses = async () => {
      try {
        setLoading(true);
        setError('');
        const response = await axios.get('/api/profile/enrolled-courses/');
        setEnrolledCourses(response.data);
      } catch (err) {
        console.error("Error fetching enrolled courses:", err);
        setError(err.response?.data?.detail || err.message || 'Failed to fetch enrolled courses.');
      } finally {
        setLoading(false);
      }
    };

    fetchEnrolledCourses();
  }, []);

  if (loading) {
    return <p>Loading enrolled courses...</p>;
  }

  if (error) {
    return <div className="alert alert-warning">{error}</div>;
  }

  if (enrolledCourses.length === 0) {
    return <p>You are not enrolled in any courses yet. <Link to="/courses">Browse courses</Link>.</p>;
  }

  return (
    <div className="mt-4">
      <h2>My Enrolled Courses</h2>
      <div className="list-group">
        {enrolledCourses.map(course => (
          <Link
            key={course.id}
            to={`/courses/${course.id}`} // Assuming a route like /courses/:id exists or will be created
            className="list-group-item list-group-item-action"
          >
            <h5 className="mb-1">{course.title}</h5>
            <p className="mb-1">{course.description?.substring(0, 100)}...</p>
            {/* Add more course details if needed */}
          </Link>
        ))}
      </div>
    </div>
  );
}

export default EnrolledCoursesList;
