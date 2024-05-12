import React , {useState, useContext}from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

import UserContext from '../UserContext';
import VenuesList from '../venue/VenuesList';
import { MATCH_INVITATION_API_URL } from '../../constants';

const MatchInvitationForm = ( ) => {
    const [scheduledDate, setScheduledDate] = useState('');
    const [scheduledTime, setScheduledTime] = useState('');
    const [selectedVenueId, setSelectedVenueId] = useState('');
    
    const { athleteId } = useParams();

    const { state } = useContext(UserContext);
    const { userId } = state;
    
    const handleSubmit = (e) => {
        e.preventDefault();
        
        axios.post(MATCH_INVITATION_API_URL, {
            sender_id: userId,
            recipient_id: athleteId,
            scheduled_date: scheduledDate,
            scheduled_time: scheduledTime,
            venue_id: selectedVenueId
        }, {
          
        }).then((response) => {
            console.log('Match invitation sent', response.data);
        }).catch((error) => {
            console.error('Error sending match invitation', error);
        });
    }; 
   

    return (
        <form onSubmit={handleSubmit}>
            <label>
                Scheduled Date:
                <input
                    type="date"
                    value={scheduledDate}
                    onChange={(e) => setScheduledDate(e.target.value)}
                />
            </label>
            <br />
            <label>
                Scheduled Time:
                <input
                    type="time"
                    value={scheduledTime}
                    onChange={(e) => setScheduledTime(e.target.value)}
                />
            </label>
            <br />
            <label>
                Venue:

                <VenuesList onVenueSelect={setSelectedVenueId} />
                
            </label>
            <br />
            <button type="submit">Submit</button>
        </form>
    );
};

export default MatchInvitationForm;