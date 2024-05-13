import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { MATCH_INVITATION_API_URL,USER_API_URL, VENUE_API_URL } from '../../constants';

const InvitationSender = ({ senderId, senderName }) => (
  <p>
    Invitation from <Link to={`/profile/${senderId}`}>{senderName}</Link>
  </p>
);

const InvitationDate = ({ date, status }) => (
  <p>
    Date: {date}
    {status === 'Accepted' && <button>Edit Date</button>}
  </p>
);

const InvitationTime = ({ time, status }) => (
  <p>
    Time: {time}
    {status === 'Accepted' && <button>Edit Time</button>}
  </p>
);

const InvitationVenue = ({ venue, status }) => (
  <p>
    Venue:<Link to={`/venue/${venue.venue_id}`}> {venue.venue_name} </Link>
    {status === 'Accepted' && <button>Edit Venue</button>}
  </p>
);

const MatchInvitationItem = ({ invitation }) => {
  const [senderUser, setSenderUser] = useState({});
  const [venue, setVenue] = useState({});
  const [changedInvitationState, setChangedInvitationState] = useState(false);
  const [isDeleted, setIsDeleted] = useState(false);

  useEffect(() => {
    async function fetchSenderUser(user_id) {
      try {
        const response = await axios.get(USER_API_URL + `${user_id}`, { withCredentials: true });
        setSenderUser(response.data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchSenderUser(invitation.sender_id);

    async function fetchVenue(venue_id) {
      try {
        const response = await axios.get(VENUE_API_URL + `${venue_id}`, { withCredentials: true });
        setVenue(response.data);
      } catch (error) {
        console.error(error);
      }
    }
    fetchVenue(invitation.venue_id);
  }, [changedInvitationState]);

  const onAccept = async () => {
    try{
      const response = await axios.put(MATCH_INVITATION_API_URL + `${invitation.invitation_id}`, { status: 'Accepted' }, { withCredentials: true });
      invitation.status = response.data.status;
      setChangedInvitationState(!changedInvitationState);
    }catch(error){
      console.error(error);
    }
  };

  const onDelete = () => {
    try{
      const confirmed = window.confirm("Are you sure you want to delete this invitation?");
      if (confirmed) {
        axios.delete(MATCH_INVITATION_API_URL + `${invitation.invitation_id}`, { withCredentials: true });
        setIsDeleted(true);
      }
    }
    catch(error){
      console.error(error);
    }
  };

  if (isDeleted) {
    return null; 
  }

  return (
    <div>
      <h2>
        <InvitationSender senderId={invitation.sender_id} senderName={senderUser.real_name} />
      </h2>
      <InvitationDate date={invitation.scheduled_date} status={invitation.status} />
      <InvitationTime time={invitation.scheduled_time} status={invitation.status} />
      <InvitationVenue venue={venue} status={invitation.status} />
      <p>Sent on: {invitation.invitation_date}</p>

      {invitation.status === 'Pending' && (
        <div>
          <button onClick={onAccept}>Accept</button>
          <button onClick={onDelete}>Delete</button>
        </div>
      )}
      {invitation.status === 'Accepted' && (
        <div>
          <button>Create match!</button>
          <button onClick={onDelete}>Cancel Invitation</button>
        </div>
      )}
    </div>
  );
};

export default MatchInvitationItem;