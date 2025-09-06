import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Modal from 'react-modal';
import ProfileCard from '../profile/ProfileCard';
import VenueCard from '../venue/VenueCard';
import { ATHLETE_API_URL, MATCH_API_URL,MATCH_INVITATION_API_URL,USER_API_URL, VENUE_API_URL } from '../../constants';

import './ModalStyles.css';

const fetchAthlete = async (athleteId) => {
  try {
    const response = await axios.get(`${ATHLETE_API_URL}${athleteId}`, { withCredentials: true });
    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

Modal.setAppElement('#root'); // This line is needed for accessibility reasons


const InvitationSender = ({ senderId, senderName }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [athlete, setAthlete] = useState(null);
  

  const openModal = async () => {
    const fetchedAthlete = await fetchAthlete(senderId);
    setAthlete(fetchedAthlete);
    console.log(fetchedAthlete)
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <p>
      Invitation from <Link onClick={openModal}>{senderName}</Link>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Athlete Card"
        className="my-modal"
        
      >
        {athlete && <ProfileCard athlete={athlete} />}
        <button onClick={closeModal}>Close</button>
      </Modal>
    </p>
  );
};



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

const InvitationVenue = ({ venue, status }) => {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  const openModal = () => {
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
  };

  return (
    <p>
      Venue: <Link onClick={openModal}>{venue.venue_name}</Link>
      {status === 'Accepted' && <button onClick={openModal}>Edit Venue</button>}

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        contentLabel="Venue Card"
        className="my-modal"
      >
        {venue && <VenueCard venue={venue} />}
        <button onClick={closeModal}>Close</button>
      </Modal>
    </p>
  );
};

const MatchInvitationItem = ({ invitation }) => {
  const [senderUser, setSenderUser] = useState({});
  const [venue, setVenue] = useState({});
  const [changedInvitationState, setChangedInvitationState] = useState(false);
  const [isDeleted, setIsDeleted] = useState(false);

  const [matchCreated, setMatchCreated] = useState(false);

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

  const onCreateMatch = () => {
    try{
      axios.post(MATCH_API_URL, 
        {
          match_date: invitation.scheduled_date,
          venue_id: invitation.venue_id,
          player1_id: invitation.sender_id,
          player2_id: invitation.recipient_id
        },
        { withCredentials: true }
      )
      .then((response) => {
        console.log(response);
        setMatchCreated(true);
      })
    }
    catch(error){
      console.error(error);
    };
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
      {invitation.status === 'Accepted'&& !matchCreated && (
        <div>
          <button onClick={onCreateMatch}>Create match!</button>
          <button onClick={onDelete}>Cancel Invitation</button>
        </div>
      )}
      {matchCreated && <p>Match successfully created!</p>}

    </div>
  );

};
export default MatchInvitationItem;