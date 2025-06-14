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

  if (loading) return <div className="loading-message">Loading poses...</div>;
  if (error) return <div className="alert alert-danger error-message">Error loading poses: {error}</div>;

  return (
    <div className="container mt-3">
      <h2 className="page-title">Yoga Poses</h2>
      {poses.length === 0 ? (
        <p className="text-center">No poses found.</p>
      ) : (
        <div className="item-list">
          {poses.map(pose => (
            <div key={pose.id} className="item-card">
              <h3>{pose.name}</h3>
              {pose.image_url && <img src={pose.image_url} alt={pose.name} />}
              <p>{pose.description}</p>
              <p><strong>Difficulty:</strong> {pose.difficulty}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Poses;
