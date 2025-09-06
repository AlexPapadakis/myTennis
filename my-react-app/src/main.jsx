import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

import {UserProvider} from './components/UserContext.jsx'; 
import './index.css'


const root = document.getElementById('root');
createRoot(root).render(
  <React.StrictMode>
    <UserProvider >
      <App />
    </UserProvider>
  </React.StrictMode>
);