import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout({onLogout}) {
    const navigate = useNavigate();

    useEffect(() => {
        onLogout(); // call the onLogout function passed as a prop
        navigate('/login'); // redirect the user to the login page
    }, [navigate]);

    return null; // this component doesn't render anything
}

export default Logout;