import React, { useReducer } from 'react';


const UserContext = React.createContext();


const userReducer = (state, action) => {
    switch (action.type) {
      case 'LOGIN':
        return { ...state, isLoggedIn: true };
      case 'LOGOUT':
        return { ...state, isLoggedIn: false, isAthlete: false, completedSignUp: false };
      case 'COMPLETED_SIGNUP':
        return { ...state, completedSignUp: true };
      case 'ATHLETE_SUBMIT':
        return { ...state, isAthlete: true };
      case 'SET_USER_DATA':
        return { ...state, ...action.payload };
      default:
        throw new Error(`Unknown action: ${action.type}`);
    }
  };
  
const UserProvider = ({ children }) => {
    const [state, dispatch] = useReducer(userReducer, {
        isLoggedIn: false,
        isAthlete: false,
        completedSignUp: false,
        city: '',
        userId: '', 
    });

    return (
        <UserContext.Provider value={{ state, dispatch }}>
        {children}
        </UserContext.Provider>
    );
}

export { UserContext, UserProvider };

export default UserContext;