import React,{useEffect, useState} from 'react';
import axios from 'axios';
import VenueCard from './VenueCard';


const VenuesList = ({ city , onVenueSelect, selectedVenueId }) => {
    const [venues, setVenues] = useState([]);

    useEffect(() => {

        axios.get(`http://localhost:8000/venues/Thessaloniki`, { 
           
        }).then((response) => {
            setVenues(response.data);
        }).catch((error) => {
            console.error('Error fetching data', error);
        });
        }, []);


   

    return (
        <div>
            <h2>Venues in {city}</h2>
            {venues.map(venue => (
               <div key={venue.venue_id}>
               <input 
                   type="radio" 
                   name="venue" 
                   value={venue.venue_id} 
                   onChange={()=>onVenueSelect(venue.venue_id)
                }   
               />
               <VenueCard venue={venue}/>
               </div>
            ))}
        </div>
    );
};


export default VenuesList;