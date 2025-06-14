import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';

function PaymentSuccess() {
  const location = useLocation();
  const [message, setMessage] = useState('Processing payment...');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const reference = queryParams.get('reference'); // Standard Paystack query param

    if (!reference) {
      setError('No payment reference found. Your payment might not have been processed correctly.');
      setIsLoading(false);
      return;
    }

    // Call your backend to verify the payment
    fetch(`/api/payment/verify/?reference=${reference}`)
      .then(response => {
        if (!response.ok) {
          // Try to parse error from backend if available
          return response.json().then(errData => {
            throw new Error(errData.error || `Server error: ${response.status}`);
          }).catch(() => {
            // Fallback if no JSON error body
            throw new Error(`Server error: ${response.status}`);
          });
        }
        return response.json();
      })
      .then(data => {
        if (data.data && data.data.status === 'success') {
          setMessage(`Payment successful! Thank you for your purchase. Transaction reference: ${data.data.reference}. You should receive a confirmation email shortly.`);
          // TODO: Add logic to enroll user or update UI accordingly
        } else {
          setError(data.message || 'Payment verification failed or payment was not successful.');
        }
        setIsLoading(false);
      })
      .catch(err => {
        console.error('Payment verification error:', err);
        setError(err.message || 'An error occurred during payment verification.');
        setIsLoading(false);
      });
  }, [location]);

  if (isLoading) {
    return <div className="container"><h1>Verifying your payment...</h1><p>Please wait.</p></div>;
  }

  return (
    <div className="container">
      <h1>Payment Status</h1>
      {error ? (
        <div className="alert alert-danger" role="alert">
          <p><strong>Error:</strong> {error}</p>
          <p>If you believe this is an error, please contact support with your payment details.</p>
        </div>
      ) : (
        <div className="alert alert-success" role="alert">
          <p>{message}</p>
        </div>
      )}
      <Link to="/courses" className="btn btn-primary">Back to Courses</Link>
      <br/>
      <Link to="/" className="btn btn-secondary mt-2">Back to Home</Link>
    </div>
  );
}

export default PaymentSuccess;
