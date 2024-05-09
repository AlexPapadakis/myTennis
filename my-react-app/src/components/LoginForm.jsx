import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginForm  ({ onLogin }) {

    const navigate = useNavigate();
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
            // localStorage.setItem('token', response.data.access_token);
            console.log(response.data);
            onLogin(); // call the function passed as a prop
            navigate('/');
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