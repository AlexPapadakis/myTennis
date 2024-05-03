import React, { useState } from 'react';
import axios from 'axios';
import { KJUR } from 'jsrsasign';

function CompleteSignUpForm({ onCompleteSignUp}) {
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) => {
        e.preventDefault();

        const city = e.target.city.value;
        const username = e.target.username.value;
        const real_name = e.target.realname.value;

        let errors = {};
        if (!city) {
            errors.city = 'City is required';
        }
        if (!username) {
            errors.username = 'Username is required';
        }

        if (!real_name) {
            errors.real_name = 'Realname is required';
        }

        if (Object.keys(errors).length > 0) {
            setErrors(errors);
        } else {
            const token = localStorage.getItem('token');
            // const decoded_token = KJUR.jws.JWS.parse(token);
            // const user_id = decoded_token.payloadObj.id;
            // const response = await axios.put(`http://localhost:8000/users/${user_id}`, {
            //     city,
            //     realname,
            //     username
            // });
            const response = await axios.put(`http://localhost:8000/users/me`, 
                {
                    city,
                    real_name,
                    username
                }, 
                {
                    headers: {
                        Authorization: `Bearer ${token}` // Include the token in the Authorization header
                    }
                });
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
                    {errors.real_name && <p>{errors.real_name}</p>}
                </label>
                <label>
                    Username
                    <input type="text" name="username" />
                    {errors.username && <p>{errors.username}</p>}
                </label>
                <label>
                    City
                    <input type="text" name="city" />
                    {errors.city && <p>{errors.city}</p>}
                </label>
                <br />
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default CompleteSignUpForm;