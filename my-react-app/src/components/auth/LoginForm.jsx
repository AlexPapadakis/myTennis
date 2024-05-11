import React, { useContext} from 'react';
import axios from 'axios';

import { UserContext } from '../UserContext';


function LoginForm  () {
    const {dispatch} = useContext(UserContext);


    const handleSubmit = (e) => {
        e.preventDefault();
        const email = e.target.email.value;
        const password = e.target.password.value;

        axios.post('http://localhost:8000/token', {
            email,
            password
        }, {
            withCredentials: true
        }).then((response) => {
            console.log(response.data);
            dispatch({ type: 'LOGIN' }); // Dispatch a 'LOGIN' action
        }).catch((error) => {
            console.error(error);
        });


    };

    return (
        <div>
        <h1>Log In</h1>
        <form onSubmit={handleSubmit}>
            <label>
                Email
                <input type="text" name="email" />
            </label>
            <label>
                Password
                <input type="password" name="password"  />
            </label>
            <button type="submit">Log In</button>
        </form>
        </div>
    );
};

export default LoginForm;