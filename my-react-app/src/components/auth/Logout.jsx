import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie'; // import js-cookie
import UserContext from '../UserContext';



function Logout() {
  const navigate = useNavigate();
  const { dispatch } = useContext(UserContext);

  const handleLogout = () => {
    const confirmLogout = window.confirm('Are you sure you want to log out?');
    if (confirmLogout) {
      axios.post('http://localhost:8000/logout', {}, { withCredentials: true })
        .then(() => {
          dispatch({ type: 'LOGOUT' });
          navigate('/login'); // redirect the user to the login page
        })
        .catch(error => {
          console.error('Error logging out', error);
        });
    } else {
      navigate('/'); // redirect the user to the home page
    }
  };

  return (
    <button onClick={handleLogout}>Logout</button>
  );
}

export default Logout;