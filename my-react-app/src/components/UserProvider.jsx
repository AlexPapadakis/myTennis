import React, { useState, useEffect } from 'react';
import axios from 'axios';
import UserContext from './UserContext';

const UserProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [completedSignUp, setCompletedSignUp] = useState(false);
  const [city, setCity] = useState(null);
  const [userId, setUserId] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/users/me/', 
    {
      withCredentials: true,
    }).then((response) => {
        setUserId(response.data.id);
        if(response.data.city != null){
          setCity(response.data.city);
        }
    }); 
  }, []);

  return (
    <UserContext.Provider value={{ isLoggedIn, setIsLoggedIn, completedSignUp, setCompletedSignUp, city, setCity, userId, setUserId }}>
      {children}
    </UserContext.Provider>
  );
}

export default UserProvider;