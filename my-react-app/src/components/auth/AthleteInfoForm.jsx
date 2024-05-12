
import React, { useState ,useContext} from 'react';
import axios from 'axios';
import UserContext from '../UserContext';

function AthleteInfoForm() {
    const [handedness, setHandedness] = useState('');
    const [height, setHeight] = useState('');
    const [backhand_type, setBackhandType] = useState('');
    const [skill_level, setSkillLevel] = useState('');

    const { state, dispatch } = useContext(UserContext);

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(handedness, height, backhand_type, skill_level);
        axios.post('http://localhost:8000/athletes/me', {
            handedness,
            height,
            backhand_type,
            skill_level
        },
            {
                withCredentials: true
            }
        ).then((response) => {
            console.log(response.data);
            dispatch({ type: 'ATHLETE_SUBMIT' });
        }
        ).catch((error) => {
            console.log(error);
        });

    };

    
    

    return (
        <div>
            <h1>Fill in your athlete information</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Height(in cm):
                    <input value={height} onChange={(e) => setHeight(e.target.value)} />
                </label>
                <label>
                    Handedness:
                    <select value={handedness} onChange={(e) => setHandedness(e.target.value)}>
                        <option value="">Select</option>
                        <option value="Right-handed">Right-handed</option>
                        <option value="Left-handed">Left-handed</option>
                    </select>
                </label>
                <br />
                <br />
                <label>
                    Backhand Type:
                    <select value={backhand_type} onChange={(e) => setBackhandType(e.target.value)}>
                        <option value="">Select</option>
                        <option value="One-handed">One-handed</option>
                        <option value="Two-handed">Two-handed</option>
                    </select>
                </label>
                <br />
                <label>
                    Skill Level:
                    <select value={skill_level} onChange={(e) => setSkillLevel(e.target.value)}>
                        <option value="">Select</option>
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate">Intermediate</option>
                        <option value="Advanced">Advanced</option>
                    </select>
                </label>
                <br />
                <button type="submit">Create Athlete profile</button>
            </form>
        </div>
    );
}

export default AthleteInfoForm;