import React,{useState} from 'react';
import axios from 'axios';



function BasicSignUpForm(){
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) =>{
        e.preventDefault();
        
        const email = e.target.email.value;
        const password = e.target.password.value;
       
       
        let errors = {};
        
        if (!email) {
            errors.email = 'Email is required';
        }
        if (!password) {
            errors.password = 'Password is required';
        }
            
        if (Object.keys(errors).length > 0) {
            setErrors(errors);
        } else {
            const response = await axios.post('http://localhost:8000/users', {
            email,
            password
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
                    <input type="text" name="email" />
                    {errors.email && <p>{errors.email}</p>} 
                </label>
                <label>
                    Password
                    <input type="password" name="password" />
                    {errors.password && <p>{errors.password}</p>}
                </label>
                <br />
                <button type="submit">Sign Up</button>
                <button type="googleSignUp">Continue with google</button>

            </form>
        </div>
    );
}

export default BasicSignUpForm;