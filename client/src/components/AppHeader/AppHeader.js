import React from 'react';
import AppHeaderAuth from '../AppHeaderAuth/AppHeaderAuth';

import logo from '../../images/microsoft_small.png';

import './AppHeader.css';

export default function AppHeader() {
  return (
    <header className="header">
      <nav className="navbar navbar-expand-lg">
        <a className="navbar-brand" href="/">
          <img src={logo} height="50" className="navbar-logo" alt="Microsoft" />
        </a>
        

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            <li className="nav-item">
              <a className="nav-link" href="/search">Search</a>
            </li>

          </ul>
        </div>

        <AppHeaderAuth />
      </nav>
      
    </header>
  );
};
