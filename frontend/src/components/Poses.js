import React, { useState, useEffect } from 'react';

function Poses() {
  const [poses, setPoses] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/poses/') // Assuming your Django API for poses is at /api/poses/
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setPoses(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Fetching poses failed:", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading poses...</div>;
  if (error) return <div>Error loading poses: {error}</div>;

  return (
    <div>
      <h2>Yoga Poses</h2>
      {poses.length === 0 ? (
        <p>No poses found.</p>
      ) : (
        <ul>
          {poses.map(pose => (
            <li key={pose.id}>
              <h3>{pose.name}</h3>
              <p>{pose.description}</p>
              <p><strong>Difficulty:</strong> {pose.difficulty}</p>
              {pose.image_url && <img src={pose.image_url} alt={pose.name} style={{maxWidth: '200px'}} />}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Poses;
