import React from "react";
import PropTypes from "prop-types";

function AthleteCard({ athlete }) {
    return (
        <div>
            <h2>{athlete.height}</h2>
            <h2>{athlete.backhand_type}</h2>
            <h2>{athlete.handedness}</h2>
            <h2>{athlete.skill_level}</h2>
            <h3>{athlete.points}</h3>
        </div>
    );
}

AthleteCard.propTypes = {
    athlete: PropTypes.shape({
        height: PropTypes.number,
        backhand_type: PropTypes.string,
        handedness: PropTypes.string,
        skill_level: PropTypes.string,
    }).isRequired,
};

export default AthleteCard;