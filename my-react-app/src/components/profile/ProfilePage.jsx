import React, { useEffect, useState } from "react";
import UserProfileCard from "./UserProfileCard";
import AthleteCard from "../athlete/AthleteCard";
import axios from  "axios";

function ProfilePage() {
    const [user, setUser] = useState();
    const [athlete, setAthlete] = useState();

    useEffect(() => {
        Promise.all([
            axios.get("http://localhost:8000/users/me/", {withCredentials: true}),
            axios.get("http://localhost:8000/athletes/me/", { withCredentials: true}) 
        ]).then(([userResponse, athleteResponse]) => {
            setUser(userResponse.data);
            athleteResponse.data.height = Number(athleteResponse.data.height);
            setAthlete(athleteResponse.data);
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

export default ProfilePage;