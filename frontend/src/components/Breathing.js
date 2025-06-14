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

  if (loading) return <div>Loading breathing exercises...</div>;
  if (error) return <div>Error loading breathing exercises: {error}</div>;

  return (
    <div>
      <h2>Breathing Exercises</h2>
      {exercises.length === 0 ? (
        <p>No breathing exercises found.</p>
      ) : (
        <ul>
          {exercises.map(exercise => (
            <li key={exercise.id}>
              <h3>{exercise.name}</h3>
              <p>{exercise.description}</p>
              <p><strong>Duration:</strong> {exercise.duration_minutes} minutes</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Breathing;
