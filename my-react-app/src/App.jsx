import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {Link} from 'react-router-dom';
import React, { useState,useEffect } from 'react';
import axios from 'axios';
import { useContext } from 'react';

import Header from './components/shared/Header.jsx'
import Footer from './components/shared/Footer.jsx'
import CompleteSignUpForm from './components/auth/CompleteSignUpForm.jsx'
import BasicSignUpForm from './components/auth/BasicSignUpForm.jsx'
import LoginForm from './components/auth/LoginForm.jsx'
import AthleteInfoForm from './components/auth/AthleteInfoForm.jsx'
import ProfilePage from './components/profile/ProfilePage.jsx'
import EditProfileInfoForm from './components/profile/EditProfileInfoForm.jsx'
import Logout from './components/auth/Logout.jsx'
import AthletesInCity from './components/athlete/AthletesInCity.jsx';
import MatchInvitationForm from './components/match/MatchInvitationForm.jsx';



import  UserContext  from './components/UserContext'; 



export const useUser = () => useContext(UserContext);


const App = () => {
  const { state, dispatch } = useUser();
  
  function renderLinks() {
    const links = [];
    if (state.isLoggedIn) {
      
      if(state.completedSignUp){
        links.push(
          <li key="editProfileInfo"><Link to="/editProfileInfo">Edit Profile Info</Link></li>
        );
          
        if (state.isAthlete) {
          links.push(
            <li key="profile"><Link to="/profile">Profile</Link></li>
          );
          links.push(
            <li key="findPlayers"><Link to="/findPlayers">Find Players</Link></li>
          );
        } else {
          links.push(
            <li key="athleteInfoForm"><Link to="/athleteInfoForm">Set up your athlete profile</Link></li>
          );
        }
    }  
      else{
        links.push(
          <li key="completeSignUp"><Link to="/signup/complete">Complete Sign Up</Link></li>
        );
      }

      links.push(
        <li key="logout"><Link to="/logout">Log out</Link></li>
      );
    } else {
      links.push(
        <li key="login"><Link to="/login">Login</Link></li>
      );
      links.push(
        <li key="signup"><Link to="/signup">Sign Up</Link></li>
      );
    }

    return links;
  }


  return (

    <Router>

    <>
    <Header />
      <nav>
        <ul>
          
            {renderLinks()}

            <Routes>
              <Route path="/login" element={<LoginForm />} />
              <Route path="/signup" element={<BasicSignUpForm />} />
              <Route path="/signup/complete" element={<CompleteSignUpForm />} />
              <Route path="/athleteInfoForm" element={<AthleteInfoForm />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/editProfileInfo" element={<EditProfileInfoForm />} />
              <Route path="/logout" element={<Logout />} />
              <Route path="/findPlayers" element={<AthletesInCity />} />
              <Route path="/matchInvitationForm/:athleteId" element={<MatchInvitationForm />} />
            </Routes>
        </ul>
      </nav>
    <hr />
    <Footer />
    </>
    </Router>

  );
}


export default App
