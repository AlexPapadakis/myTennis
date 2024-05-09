import React, { useState, useEffect } from 'react';
import ProfileCard from './ProfileCard';
import axios from 'axios';

import { useNavigate } from 'react-router-dom';
import { useContext ,createContext} from 'react';

import UserContext from './UserContext';


const AthletesInCity = () => {
    const [athletes, setAthletes] = useState([]);
    const [skillLevelFilter, setSkillLevelFilter] = useState('');

    const { city } = useContext(UserContext);

    const navigate = useNavigate()

    useEffect(() => {
        axios.get(`http://localhost:8000/athletes?city=${city}`, {
            withCredentials: true
        }).then((response) => {
            setAthletes(response.data);
        }).catch((error) => {
            console.error('Error fetching data', error);
        });
    }, [city]);


   
    const handleInviteClick = (athleteId) => {
        navigate(`/matchInvitationForm/${athleteId}`);
        };
    

       

    const handleSkillLevelFilterChange = (event) => {
        setSkillLevelFilter(event.target.value);
    };

    const filteredAthletes = athletes.filter((athlete) => {
        return (athlete.skill_level === skillLevelFilter || skillLevelFilter === '');
    });

    return (
        <div>
            <h2>Athletes in {city}</h2>
            <div>
                <label htmlFor="skill-level-filter">Skill Level:</label>
                <select id="skill-level-filter" value={skillLevelFilter} onChange={handleSkillLevelFilterChange}>
                    <option value="">All</option>
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                </select>
            </div>
            
            

            {filteredAthletes.map((athlete) => (
                <div key={athlete.user_id}>
                    <ProfileCard athlete={athlete} />
                    <button onClick={() => handleInviteClick(athlete.user_id)}>Invite to match</button>
                </div>
            ))}
      

        </div> );
};

export default AthletesInCity;
