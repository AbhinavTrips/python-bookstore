import React, {useState, useEffect} from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import axios from 'axios';

// Context for user authentication
import { AuthContext } from '../contexts/AuthContext';

// App shell components
import AppHeader from '../components/AppHeader/AppHeader';
import AppFooter from '../components/AppFooter/AppFooter';

// React Router page components
//import Home from '../pages/Home/Home';
import Search from '../pages/Search/Search';
import Details from '../pages/Details/Details';

// Bootstrap styles, optionally with jQuery and Popper
import 'bootstrap/dist/css/bootstrap.min.css';

// Custom app styles
import './App.css';

export default function App() {
  // React Hook: useState with a var name, set function, & default value
  
  const [ resultCount, setResultCount ] = useState(0);




  async function setAllBooksCount() {
    axios.get( 'http://localhost:8000/get_items_count')
        .then(response => {
            console.log("Setting result count: "+response.data.count);
            setResultCount(response.data.count);
          } )
          .catch(error => {
              console.log(error);
          });
  }

  // React Hook: useEffect when component changes
  // Empty array ensure this only runs once on mount
  useEffect(() => {
    setAllBooksCount()
  }, []);

  return (
    
      <div className="container-fluid app">
        <AppHeader />
        <BrowserRouter>
          <Routes>
            <Route path={`/`} element={<Search resultCount={resultCount}/>} />
            <Route path={`/search`} element={<Search resultCount={resultCount} />} />
            <Route path={`/details/:id/:isbn10`} element={<Details />}/>
            <Route path={`*`} element={<Search />} />
          </Routes>
        </BrowserRouter>
        {<AppFooter />}
      </div>
  );
}
