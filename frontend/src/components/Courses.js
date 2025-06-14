import React, { useState, useEffect } from 'react';

function Courses() {
  const [courses, setCourses] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [paymentError, setPaymentError] = useState(null);

  const handleInitiatePayment = (courseId) => {
    setPaymentError(null); // Clear previous payment errors
    // Note: This assumes the user is logged in.
    // In a real app, you'd get the auth token. For now, relying on session/cookie.
    fetch('/api/payment/initiate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': `Token ${yourAuthToken}` // Add if your endpoint is protected
      },
      body: JSON.stringify({ course_id: courseId })
    })
    .then(response => {
      if (!response.ok) {
        return response.json().then(err => { throw new Error(err.error || 'Payment initiation failed') });
      }
      return response.json();
    })
    .then(data => {
      if (data.authorization_url) {
        window.location.href = data.authorization_url; // Redirect to Paystack
      } else {
        throw new Error('No authorization URL received from Paystack.');
      }
    })
    .catch(err => {
      console.error("Payment initiation error:", err);
      setPaymentError(err.message);
    });
  };

  useEffect(() => {
    fetch('/api/courses/') // Assuming API endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setCourses(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Fetching courses failed:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading-message">Loading courses...</div>;
  if (error) return <div className="alert alert-danger error-message">Error loading courses: {error}</div>;

  return (
    <div className="container mt-3">
      <h2 className="page-title">Yoga Courses</h2>
      {paymentError && <div className="alert alert-danger error-message mt-3">Payment Error: {paymentError}</div>}
      {courses.length === 0 ? (
        <p className="text-center">No courses found.</p>
      ) : (
        <div className="item-list">
          {courses.map(course => (
            <div key={course.id} className="item-card">
              <h3>{course.title}</h3>
              <p>{course.description}</p>
              <p><strong>Price:</strong> ${course.price}</p>
              <h5>Poses:</h5>
              {course.poses && course.poses.length > 0 ? (
                <ul className="list-styled mb-2">
                  {course.poses.map(pose => <li key={pose.id}>{pose.name}</li>)}
                </ul>
              ) : <p>No poses listed for this course.</p>}
              <h5>Breathing Exercises:</h5>
              {course.breathing_exercises && course.breathing_exercises.length > 0 ? (
                <ul className="list-styled mb-2">
                  {course.breathing_exercises.map(exercise => <li key={exercise.id}>{exercise.name}</li>)}
                </ul>
              ) : <p>No breathing exercises listed for this course.</p>}
              <button
                onClick={() => handleInitiatePayment(course.id)}
                className="btn btn-success w-100" // Full width button
              >
                Buy Course (${course.price})
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Courses;
