import React,{useState} from 'react';
import axios from 'axios';



function CompleteSignUpForm(){
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) =>{
        e.preventDefault();
        
        const city = e.target.city.value;
        const username = e.target.username.value;
        const realname = e.target.realname.value;
       
        let errors = {};
        if (!city) {
            errors.city = 'City is required';
        }
        if (!username) {
            errors.username = 'Username is required';
        }
        if (!realname) {
            errors.realname = 'Realname is required';
        }
            
        if (Object.keys(errors).length > 0) {
            setErrors(errors);
        } else {
            const response = await axios.put('http://localhost:8000/users', {
            city,
            realname,
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
                    Real Name
                    <input type="text" name="realname" />
                    {errors.realname && <p>{errors.realname}</p>}
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
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default CompleteSignUpForm;