import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

import EditableField from "../shared/EditableField";


const userFields = [
    { label: "Username", fieldName: "username" },
    { label: "Email", fieldName: "email" },
    { label: "Real Name", fieldName: "real_name" },
    { label: "Gender", fieldName: "gender" ,type: "select",options: ['Male','Female','Other']},
    { label: "Phone", fieldName: "phone" },
    { label: "City", fieldName: "city" ,type:"select",options:["Thessaloniki"]},
    { label:"Address",fieldName:"address" },
    { label: "Postal Code", fieldName: "postal_code" },
    { label: "Birthday", fieldName: "birthday",type:"date"}
];

const athleteFields = [
    { label: "height", fieldName: "height" },
    { label: "Handedness", fieldName: "handedness", type: "select", options: ['Right-handed', 'Left-handed'] },
    { label: "Backhand Type", fieldName: "backhand_type", type: "select", options: ['One-handed', 'Two-handed'] },
    { label: "Skill Level", fieldName: "skill_level", type: "select", options: ['Beginner', 'Intermediate', 'Advanced'] },
];

function EditProfileInfoForm() {
  const [user, setUser] = useState('');
  const [athlete, setAthlete] = useState('');
  const [message, setMessage] = useState(''); 
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const userResponse = await axios.get("http://localhost:8000/users/me/", { withCredentials: true });
        setUser(userResponse.data);

        const athleteResponse = await axios.get("http://localhost:8000/athletes/me/", { withCredentials: true });
        setAthlete(athleteResponse.data);
      } catch (error) {
        if (error.response && error.response.status === 404) {
          setMessage("Please set up your athlete profile");
        } else {
          setError("Error fetching data");
        }
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      {error && <p>{error}</p>}
      {user && (
        <>
          <h1>Edit user Information</h1>
          <img src="default-profile-picture.png" alt="Profile" />
          {userFields.map(field => (
            <EditableField
              key={field.fieldName}
              label={field.label}
              initialValue={user[field.fieldName]}
              className="user"
              fieldName={field.fieldName}
              type={field.type}
              options={field.options}
            />
          ))}
        </>
      )}
      {message && <li><Link to="/athleteInfoForm">Set up your athlete profile</Link></li>}
      {athlete && (
        <>
          <h1>Edit athlete info</h1>
          {athleteFields.map(field => (
            <EditableField
              key={field.fieldName}
              label={field.label}
              initialValue={athlete[field.fieldName]}
              className="athlete"
              fieldName={field.fieldName}
              type={field.type}
              options={field.options}
            />
          ))}
        </>
      )}
    </div>
  );
}

export default EditProfileInfoForm;