import React, { useState,useContext } from 'react';
import axios from 'axios';
import { KJUR } from 'jsrsasign';
import UserContext from '../UserContext';

function CompleteSignUpForm({ }) {

    const {dispatch}  = useContext(UserContext);
    const handleSubmit = async (e) => {
        e.preventDefault();

        const city = e.target.city.value;
        const username = e.target.username.value;
        const real_name = e.target.realname.value;

        if(city && real_name && username){
        const response = await axios.put(`http://localhost:8000/users/me`, 
            {
                city,
                real_name,
                username
            }, 
            {
                withCredentials: true
            });
        dispatch({ type: 'COMPLETED_SIGNUP' })
        dispatch({ type: 'SET_USER_DATA', payload: { city } });

        console.log(response.data);
       }
    };

    return (
        <div>
            <h1>Complete Basic Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Real Name
                    <input type="text" name="realname" />
                </label>
                <label>
                    Username
                    <input type="text" name="username" />
                </label>
                <label>
                    City
                    <input type="text" name="city" />
                </label>
                <br />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default CompleteSignUpForm;