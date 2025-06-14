import React from 'react';

function Footer() {
  return (
    <footer className="footer">
      <div className="container">
        <p>&copy; {new Date().getFullYear()} Yoga App. All Rights Reserved.</p>
        {/* Optional: Add more links or info here */}
      </div>
    </footer>
  );
}

export default Footer;
