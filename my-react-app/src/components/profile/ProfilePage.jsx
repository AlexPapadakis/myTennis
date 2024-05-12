import React, { useEffect, useState } from "react";
import UserProfileCard from "./UserProfileCard";
import AthleteCard from "../athlete/AthleteCard";
import axios from  "axios";
import { CURRENT_ATHLETE_API_URL, CURRENT_USER_API_URL } from "../../constants";

function ProfilePage() {
    const [user, setUser] = useState();
    const [athlete, setAthlete] = useState();

    useEffect(() => {
        Promise.all([
            axios.get(CURRENT_USER_API_URL, {withCredentials: true}),
            axios.get(CURRENT_ATHLETE_API_URL, { withCredentials: true}) 
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