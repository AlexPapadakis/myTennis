import Header from './components/Header.jsx'
import Footer from './components/Footer.jsx'
import SignUpForm from './components/SignUpForm.jsx'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';


import {Link} from 'react-router-dom';

function App() {
  return (
    <>
    <Header />
      <nav>
        <ul>
          <li><a href="#">Login</a></li>
          
          <Router>
            <li><Link to="/signup">Sign Up</Link></li>
            <Routes>
              <Route path="/signup" element={<SignUpForm />} />
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
