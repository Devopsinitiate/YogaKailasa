import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/poses">Poses</Link></li>
        <li><Link to="/breathing">Breathing Exercises</Link></li>
        <li><Link to="/courses">Courses</Link></li>
      </ul>
    </nav>
  );
}

export default Navbar;
