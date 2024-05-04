import React, { useState, useEffect } from 'react';
import ProfileCard from './ProfileCard';
import axios from 'axios';

const AthletesInCity = ({ city }) => {
    const [athletes, setAthletes] = useState([]);
    const [skillLevelFilter, setSkillLevelFilter] = useState('');

    useEffect(() => {
        axios.get(`http://localhost:8000/athletes?city=${city}`, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`
            }
        }).then((response) => {
            setAthletes(response.data);
        });
    }, [city]);

    const sendInvite = (athleteId) => {
        // Logic to send invite to the player
        console.log(`Sending invite to athlete with ID: ${athleteId}`);
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
                    <button onClick={() => sendInvite(athlete.id)}>Invite</button>
                </div>
            ))}
        </div>
    );
};

export default AthletesInCity;
