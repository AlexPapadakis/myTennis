import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import EditableField from "./EditableField";


function EditProfileInfoForm() {
    
    const [user, setUser] = useState('');
    const [athlete, setAthlete] = useState('');

    const [message, setMessage] = useState(''); 

    useEffect(() => {

    
        axios.get("http://localhost:8000/users/me/",  { withCredentials: true})
            .then(response => {
                setUser(response.data);
            })
            .catch(error => {
                console.error("Error fetching user data: ", error);
            });
    
        axios.get("http://localhost:8000/athletes/me/", { withCredentials: true })
            .then(response => {
                setAthlete(response.data);
            })
            .catch(error => {
                if (error.response && error.response.status === 404) {
                    console.log("Athlete not found");
                    setMessage("Please set up your athlete profile"); // Update the message state
                } else {
                    console.error("Error fetching athlete data: ", error);
                }
            });
    }, []);

    return (
        <div>
            {user && (
                <>
                    <h1>Edit user Information</h1>
                    <img src="default-profile-picture.png" alt="Profile" />                 
                    <EditableField label="Username" initialValue={user.username} className="user" fieldName="username" />
                    <EditableField label="Email" initialValue={user.email} className="user" fieldName="email" />
                    <EditableField label="Real Name" initialValue={user.real_name} className="user" fieldName="real_name" />
                    <EditableField label="Gender" initialValue={user.gender} className="user" fieldName="gender" type="select" options = {['Male', 'Female', 'Other']} />
                    <EditableField label="Phone" initialValue={user.phone} className="user" fieldName="phone" />
                    <EditableField label="Birthday" initialValue={user.birthday} className="user" fieldName="birthday" type= "date"/>
                    <EditableField label="Address" initialValue={user.address} className="user" fieldName="address" />
                    <EditableField label="City" initialValue={user.city} className="user" fieldName="city" type="select" options={['Thessaloniki']}/>
                    <EditableField label="Postal Code" initialValue={user.postal_code} className="user" fieldName="postal_code" />
                </>
            )}
        
            {message &&<li><Link to="/athleteInfoForm">Set up your athlete profile</Link></li>}
            {athlete && (
                <>
                    <h1>Edit athlete info</h1>
                    <EditableField label="Handedness" initialValue={athlete.handedness} className="athlete" fieldName="handedness"  type="select" options = { ['Right-handed', 'Left-handed']} />
                    <EditableField label="Height" initialValue={athlete.height} className="athlete" fieldName="height" />
                    <EditableField label="Backhand Type" initialValue={athlete.backhand_type} className="athlete" fieldName="backhand_type"  type="select" options = {['One-handed', 'Two-handed']} />
                    <EditableField label="Skill Level" initialValue={athlete.skill_level} className="athlete" fieldName="skill_level" type="select" options = {['Beginner', 'Intermediate', 'Advanced']} />
                </>
            )}
        </div>
    );
}

export default EditProfileInfoForm;