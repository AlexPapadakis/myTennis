import React from 'react';
import PropTypes from 'prop-types';

function UserProfileCard({user}) {
    return (
        <div>
            <h1>{user.real_name}</h1>
            <h2>#{user.username}</h2>
            <img src="default-profile-picture.png" alt="Profile" /> 

        </div>
    );
}

UserProfileCard.propTypes = {
    user: PropTypes.shape({
        real_name: PropTypes.string,
        username: PropTypes.string,
        profile_pic: PropTypes.string,
    }).isRequired,
};


export default UserProfileCard;