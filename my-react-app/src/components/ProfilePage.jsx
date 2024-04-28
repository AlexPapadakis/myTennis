import React, { useEffect, useState } from "react";
import UserProfileCard from "./UserProfileCard";
import AthleteCard from "./AthleteCard";
import axios from  "axios";

function ProfilePage() {
    const [user, setUser] = useState('');
    const [athlete, setAthlete] = useState('');

    useEffect(() => {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        Promise.all([
            axios.get("http://localhost:8000/users/me/", { headers }),
            axios.get("http://localhost:8000/athletes/me/", { headers }) // replace with your actual API endpoint
        ]).then(([userResponse, athleteResponse]) => {
            setUser(userResponse.data);
            setAthlete(athleteResponse.data);
        }).catch((error) => {
            console.error(error);
        });
    }, []);

    return (
        <div>
            <UserProfileCard user={user} />
            <AthleteCard athlete={athlete} />
        </div>
    );
}

export default ProfilePage;