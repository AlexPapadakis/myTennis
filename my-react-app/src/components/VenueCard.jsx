import React from 'react';


const VenueCard = ({ venue }) => {
    return (
        <div>
            <h2>{venue.venue_name}</h2>
            <img src={"default-venue-picture.png"} alt={"Venue"} />
            <p>{venue.surface_type}</p>
            <p>{venue.venue_city}</p>
            <p>{venue.venue_address}</p>
            <p>{venue.google_maps_url}</p>
        </div>
    );
};



export default VenueCard;