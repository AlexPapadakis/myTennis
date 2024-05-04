import React, { useEffect, useState } from "react";
import UserProfileCard from "./UserProfileCard";
import AthleteCard from "./AthleteCard";
import axios from  "axios";

function ProfileCard({athlete}) {
    const [user, setUser] = useState();
    console.log(athlete);
    useEffect(() => {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        Promise.all([
            axios.get(`http://localhost:8000/users/${athlete.user_id}`, { headers }),
        ]).then(([userResponse]) => {
            setUser(userResponse.data);
        }).catch((error) => {
            console.error(error);
        });
    }, []);

    return (
        <div>
            {user && <UserProfileCard user={user} />}
            {athlete && <AthleteCard athlete={athlete} />}
        </div>
    );
}

export default ProfileCard;