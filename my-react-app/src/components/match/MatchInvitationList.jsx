import React from 'react';
import MatchInvitationItem from './MatchInvitationItem';
import { useState,useEffect } from 'react';
import { MY_MATCH_INVITATIONS_API_URL } from '../../constants';
import axios from 'axios';

const MatchInvitationList = () => {

    const [invitations, setInvitations] = useState([]);

    

useEffect(() => {
  // This function fetches the invitations and the sender user for each invitation
  const fetchInvitations = async () => {
    try {
      // Fetch the invitations
      const response = await axios.get(MY_MATCH_INVITATIONS_API_URL, { withCredentials: true });
      const invitations = response.data;

      setInvitations(invitations);
    } catch (error) {
      console.error(error);
    }
  };

  // Call the fetchInvitations function
  fetchInvitations();
}, []); 
    
    return (
      <div>
        <h2>Your Invitations</h2>
        {invitations.map(invitation => (
          <MatchInvitationItem key={invitation.invitation_id} invitation={invitation}/>
        ))}
      </div>
    );
  }

export default MatchInvitationList;