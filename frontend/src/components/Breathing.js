import React, { useState, useEffect } from 'react';

function Breathing() {
  const [exercises, setExercises] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/breathing-exercises/') // Assuming API endpoint
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setExercises(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Fetching breathing exercises failed:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="loading-message">Loading breathing exercises...</div>;
  if (error) return <div className="alert alert-danger error-message">Error loading breathing exercises: {error}</div>;

  return (
    <div className="container mt-3">
      <h2 className="page-title">Breathing Exercises</h2>
      {exercises.length === 0 ? (
        <p className="text-center">No breathing exercises found.</p>
      ) : (
        <div className="item-list">
          {exercises.map(exercise => (
            <div key={exercise.id} className="item-card">
              <h3>{exercise.name}</h3>
              <p>{exercise.description}</p>
              <p><strong>Duration:</strong> {exercise.duration_minutes} minutes</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Breathing;
