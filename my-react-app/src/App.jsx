import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import CompleteSignUpForm from './components/CompleteSignUpForm.jsx'
import BasicSignUpForm from './components/BasicSignUpForm.jsx'
import LoginForm from './components/LoginForm.jsx'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import AllUsers from './components/all_users.jsx'
import {Link} from 'react-router-dom';

function App() {
  return (
    <>
    <Header />
      <nav>
        <ul>
          <Router>
          <li><Link to="/login">Login</Link></li>        
          <li><Link to="/signup">Sign Up</Link></li>

          <li><Link to="/users/"  >Users</Link></li>
            <Routes>
              <Route path="/login" element={<LoginForm />} />
              <Route path="/signup" element={<BasicSignUpForm />} />
              <Route path="/signup/complete" element={<CompleteSignUpForm />} />

              <Route path="/users/" element={<AllUsers />} />
            </Routes>
          </Router>
  
          <li><a href="#">Your profile</a></li>
        </ul>
      </nav>
    <hr />
    <Footer />
    </>
  );
}

export default App
