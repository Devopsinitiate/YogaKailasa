import React from 'react';
import { Link } from 'react-router-dom';

function PaymentFailure() {
  return (
    <div className="container">
      <h1>Payment Failed</h1>
      <div className="alert alert-danger" role="alert">
        <p>Unfortunately, your payment could not be processed at this time.</p>
        <p>Please try again or use a different payment method. If the problem persists, contact our support.</p>
      </div>
      <Link to="/courses" className="btn btn-primary">Try Another Course</Link>
      <br/>
      <Link to="/" className="btn btn-secondary mt-2">Back to Home</Link>
    </div>
  );
}

export default PaymentFailure;
