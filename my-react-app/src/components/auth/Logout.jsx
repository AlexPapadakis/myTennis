import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

import { useContext } from 'react';
import UserContext from '../UserContext';

function Logout() {
    const navigate = useNavigate();


    const { dispatch } = useContext(UserContext);
    useEffect(() => {
        dispatch({ type: 'LOGOUT' }); 
        navigate('/login'); // redirect the user to the login page
    }, [navigate]);

    return null; // this component doesn't render anything
}

export default Logout;