
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import {Link} from 'react-router-dom';
import React, { useState,useEffect } from 'react';
import axios from 'axios';

import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import CompleteSignUpForm from './components/CompleteSignUpForm.jsx'
import BasicSignUpForm from './components/BasicSignUpForm.jsx'
import LoginForm from './components/LoginForm.jsx'
import AthleteInfoForm from './components/AthleteInfoForm.jsx'
import ProfilePage from './components/ProfilePage.jsx'
import EditProfileInfoForm from './components/EditProfileInfoForm.jsx'
import Logout from './components/Logout.jsx'
import AthletesInCity from './components/AthletesInCity.jsx';

import MatchInvitationForm from './components/MatchInvitationForm.jsx';

import  UserProvider  from './components/UserProvider';

function App() {

  const [isLoggedIn, setIsLoggedIn] = useState(true)
  const [completedSignUp,setCompletedSignUp] = useState('')
  const [isAthlete, setIsAthlete] = useState(false)
  const [city, setCity] = useState(null)

 
  

  const handleLogin = () => {
    setIsLoggedIn(true);
  };
  const handleLogout = () => {  
    setIsLoggedIn(false);
  };
  const handleAthleteSubmit = () => {
    setIsAthlete(true);
  };
  const handleCompleteSignUpSubmit = () => {
    setCompletedSignUp(true);
  };
  

  
  useEffect (() => {
      axios.get('http://localhost:8000/users/me/', 
      {
        withCredentials: true,
      }).then((response) => {
      console.log(response)
       if (response.data.city==null
            &&response.data.username==null
            &&response.data.real_name==null){
          console.log('not completed')
          setCompletedSignUp(false)
        }
        else{
          console.log('completed')
          setCompletedSignUp(true)
          setCity(response.data.city);        }
      }
      ).catch((error) => {
        if (error.response && error.response.status === 401) {
          setIsLoggedIn(false);
        }else{
          console.log(error);
        }
      });
  }
  , [isLoggedIn,completedSignUp]);


  useEffect (() => {
    if(isLoggedIn){
      axios.get('http://localhost:8000/athletes/me/', {
        withCredentials: true,
        })
      .then((response) => { 
        if (response.data.height==null
            ||response.data.handedness==null
            ||response.data.backhand_type==null
            ||response.data.skill_level==null){
          setIsAthlete(false)
        }
        else{
          setIsAthlete(true)
        }
        
      }
      ).catch((error) => {
        console.log(error);
      }); 
    }
  }
  , [isLoggedIn,isAthlete]);



  return (

    <Router>

    <UserProvider >
    <>
    <Header />
      <nav>
        <ul>
            
            {isLoggedIn && isAthlete && <li><Link to="/profile">Profile</Link></li>}
            {isLoggedIn && <li><Link to="/editProfileInfo">Edit Profile Info</Link></li>}
            {!isLoggedIn && <li><Link to="/login">Login</Link></li>}
            {!isLoggedIn && <li><Link to="/signup">Sign Up</Link></li>}
            {!completedSignUp && isLoggedIn && <li><Link to="/signup/complete">Complete Sign Up</Link></li>}            
            {!isAthlete && isLoggedIn && <li><Link to="/athleteInfoForm">Set up your athlete profile</Link></li>}
            {isLoggedIn&&<li><Link to="/logout">Log out</Link></li>}
            {isLoggedIn && completedSignUp && isAthlete && <li><Link to="/findPlayers">Find Players</Link></li>}
            
            <Routes>
              <Route path="/login" element={<LoginForm onLogin={handleLogin}/>} />
              <Route path="/signup" element={<BasicSignUpForm />} />
              <Route path="/signup/complete" element={<CompleteSignUpForm onCompleteSignUp={handleCompleteSignUpSubmit}/>} />
              <Route path="/athleteInfoForm" element={<AthleteInfoForm onAthleteInfoSubmit={handleAthleteSubmit} />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/editProfileInfo" element={<EditProfileInfoForm />} />
              <Route path="/logout" element={<Logout  onLogout={handleLogout} />} />


              <Route path="/findPlayers" element={<AthletesInCity />} />
              <Route path="/matchInvitationForm/:athleteId" element={<MatchInvitationForm />} />
            </Routes>
  
        </ul>
      </nav>
    <hr />
    <Footer />
    </>
    </UserProvider>
    </Router>

  );
}


export default App
