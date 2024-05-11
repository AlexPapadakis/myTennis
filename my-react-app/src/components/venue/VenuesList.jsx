import React,{useEffect, useState,useContext} from 'react';
import axios from 'axios';
import VenueCard from './VenueCard';

import UserContext from '../UserContext';

const VenuesList = ({ onVenueSelect}) => {
    const [venues, setVenues] = useState([]);


    const { state } = useContext(UserContext);
    useEffect(() => {

        axios.get(`http://localhost:8000/venues/city/${state.city}`, { 
           
        }).then((response) => {
            setVenues(response.data);
        }).catch((error) => {
            console.error('Error fetching data', error);
        });
        }, []);



    return (
        <div>
            <h2>Venues in {state.city}</h2>
            {venues.map(venue => (
               <div key={venue.venue_id}>
               <input 
                   type="radio" 
                   name="venue" 
                   value={venue.venue_id} 
                   onChange={(e) => {
                    if (e.target.checked) {
                        onVenueSelect(venue.venue_id);
                    }
                }}                  
               />
               <VenueCard venue={venue}/>
               </div>
            ))}
        </div>
    );
};


export default VenuesList;