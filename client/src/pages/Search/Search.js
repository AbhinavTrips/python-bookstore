import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CircularProgress  from '@mui/material/CircularProgress';
import { useLocation, useNavigate } from "react-router-dom";

import Results from '../../components/Results/Results';
import Pager from '../../components/Pager/Pager';
import SearchBar from '../../components/SearchBar/SearchBar';

import "./Search.css";

export default function Search(props) {
  
  let location = useLocation();
  const navigate = useNavigate();
  
  const [ queryType, setQueryType] = useState('normal');
  const [ results, setResults ] = useState([]);
  const [ currentPage, setCurrentPage ] = useState(1);
  const [ q, setQ ] = useState(new URLSearchParams(location.search).get('q') ?? "");
  const [ top ] = useState(new URLSearchParams(location.search).get('top') ?? 10);
  const [ skip, setSkip ] = useState(new URLSearchParams(location.search).get('skip') ?? 0);
  const [ isLoading, setIsLoading ] = useState(true);

  let resultsPerPage = top;
  const resultCount = props.resultCount;
  
  
  
  useEffect(() => {
    setIsLoading(true);
    setSkip((currentPage-1) * top);

  if (q === '' ) {  
    setQueryType('normal');
    console.log("Executing normal query"+ queryType)
    axios.get( 'http://localhost:8000/list_books_by_page?limit='+top+'&page_offset='+skip)
        .then(response => {              
              setResults(response.data.results);
              setIsLoading(false);
          } )
          .catch(error => {
              console.log(error);
              setIsLoading(false);
          });

  } else {
    setQueryType('vector'+queryType);
    console.log("Executing vector search")
    axios.get( 'http://localhost:8000/get_vector_search_results?search_text='+q)
        .then(response => {
              setResults(response.data.results);
              setIsLoading(false);
          } )
          .catch(error => {
              console.log(error);
              setIsLoading(false);
          });
      
    }

}, [q, top, skip, currentPage]);

  // pushing the new search term to history when q is updated
  // allows the back button to work as expected when coming back from the details page
  useEffect(() => {
    navigate('/search?q=' + q );  
    setCurrentPage(1);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [q]);


  let postSearchHandler = (searchTerm) => {
    //console.log(searchTerm);
    setQ(searchTerm);
  }

  var body;
  if (isLoading) {
    body = (
      <div className="col-md-9">
        <CircularProgress />
      </div>);
  } else if (queryType === 'normal') {
    body = (
      <div className="col-md-9">
        <Results documents={results} top={top} skip={skip} count={resultCount} queryType={queryType}></Results>
        <Pager className="pager-style" currentPage={currentPage} resultCount={resultCount} resultsPerPage={resultsPerPage} setCurrentPage={setCurrentPage}></Pager>
      </div>
    )
  } else {
    body = (
      <div className="col-md-9">
        <Results documents={results} top={top} skip={skip} count={resultCount} queryType={queryType}></Results>
      </div>
    )
  }

  return (
    <main className="main main--search container-fluid">
      <div className="row">
        <div className="col-md-3">
          <div className="search-bar">
            <SearchBar postSearchHandler={postSearchHandler} q={q}></SearchBar>
          </div>
        </div>
        {body}
      </div>
    </main>
  );
}
