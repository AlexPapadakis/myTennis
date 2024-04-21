import React,{useState} from 'react';
import axios from 'axios';



function SignUpForm(){
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) =>{
        e.preventDefault();
        const email = e.target.email.value;
        const password = e.target.password.value;
        const city = e.target.city.value;
        const phone = e.target.phone.value;
        const username = e.target.username.value;
    
        let errors = {};
        if (!email) {
        errors.email = 'Email is required';
        }

        if (!password) {
        errors.password = 'Password is required';
        }
        if (!city) {
            errors.city = 'City is required';
        }
        if (!phone) {
            errors.phone = 'Phone is required';
        }
        if (!username) {
            errors.username = 'Username is required';
        }
            
        if (Object.keys(errors).length > 0) {
            setErrors(errors);
        } else {
            const response = await axios.post('http://localhost:8000/users', {
            email,
            password,
            city,
            phone,
            username
            });
            console.log(response.data);
            }
    };

    return (
        <div>
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Email
                    <input type="email" name="email" />
                    {errors.email && <p>{errors.email}</p>}
                </label>
                <label>
                    Password
                    <input type="password" name="password" />
                    {errors.password && <p>{errors.password}</p>}
                </label>
                <label>
                    City
                    <input type="text" name="city" />
                    {errors.city && <p>{errors.city}</p>}
                </label>
                <label>
                    Phone
                    <input type="text" name="phone" />
                    {errors.phone && <p>{errors.phone}</p>}
                </label>
                <label>
                    Username
                    <input type="text" name="username" />
                    {errors.username && <p>{errors.username}</p>}
                </label>
                <br />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignUpForm;