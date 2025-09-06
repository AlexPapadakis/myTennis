import React, { useReducer ,useEffect} from 'react';
import axios from 'axios';
import { CURRENT_USER_API_URL, CURRENT_ATHLETE_API_URL } from '../constants';

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
    
  const checkUserDataComplete = (data) => 
    data.city !== null && data.username !== null && data.real_name !== null;
  
  const checkAthleteDataComplete = (data) => 
    data.height !== null && data.handedness !== null && data.backhand_type !== null && data.skill_level !== null;
  
  const { isLoggedIn, isAthlete, completedSignUp, city, userId } = state;


  useEffect(() => {
    const fetchData = async () => {
        try {
          const userResponse = await axios.get(CURRENT_USER_API_URL, { withCredentials: true });
          const athleteResponse = await axios.get(CURRENT_ATHLETE_API_URL, { withCredentials: true });

          dispatch({
            type: 'SET_USER_DATA',
            payload: {
              userId: userResponse.data.id,
              completedSignUp: checkUserDataComplete(userResponse.data),
              city: userResponse.data.city,
              isAthlete: checkAthleteDataComplete(athleteResponse.data),
            },
          });
        } catch (error) {
          if (error.response && error.response.status === 401) {
            dispatch({ type: 'LOGOUT' });
          } else {
            console.error(error);
          }
        }
    };

    fetchData();
  }, [isLoggedIn,isAthlete,completedSignUp]);


    return (
        <UserContext.Provider value={{ state, dispatch }}>
        {children}
        </UserContext.Provider>
    );
}

export { UserContext, UserProvider };

export default UserContext;