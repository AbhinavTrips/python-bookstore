import React, { useState, useEffect } from "react";
import { useParams } from 'react-router-dom';
import Rating from '@mui/material/Rating';
import CircularProgress from '@mui/material/CircularProgress';
import axios from 'axios';

import "./Details.css";

export default function Details() {

  let { id, isbn10 } = useParams();
  const [document, setDocument] = useState({});
  const [selectedTab, setTab] = useState(0);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
     console.log('ISBN'+isbn10);
    
     //axios.get('/api/lookup?id=' + id)
    axios.get('http://localhost:8000/getBookById?id=' + id+ '&isbn10=' + isbn10)
      .then(response => {
        console.log("Success")
        console.log(JSON.stringify(response.data))
        const doc = response.data;
        setDocument(doc);
        setIsLoading(false);
      })
      .catch(error => {
        console.log("Failed")
        console.log(error);
        setIsLoading(false);
      });
  }, [id, isbn10]);

  // View default is loading with no active tab
  let detailsBody = (<CircularProgress />),
      resultStyle = "nav-link",
      rawStyle    = "nav-link";


  if (!isLoading && document) {
    console.log(`document = ${JSON.stringify(document)}`);
    // View result
    if (selectedTab === 0) {
      resultStyle += " active";
      detailsBody = (
        <div className="card-body">
          <h5 className="card-title">{document.original_title}</h5>
          <img className="image" src={document.thumbnail} alt="Book cover"></img>
          <p className="card-text">{document.authors?.join('; ')} - {document.original_publication_year}</p>
          <p className="card-text">ISBN {document.isbn}</p>
          <Rating name="half-rating-read" value={parseInt(document.average_rating)} precision={0.1} readOnly></Rating>
          <p className="card-text">{document.ratings_count} Ratings</p>
        </div>
      );
    }

    // View raw data
    else {
      rawStyle += " active";
      detailsBody = (
        <div className="desc">
          
            {document.description}
         
        </div>
      );
    }
  }

  return (
    <main className="main main--details container fluid">
      <div className="card text-center result-container">
        <div className="card-header">
          <ul className="nav nav-tabs card-header-tabs">
              <li className="nav-item"><button className={resultStyle} onClick={() => setTab(0)}>Result</button></li>
              <li className="nav-item"><button className={rawStyle} onClick={() => setTab(1)}>Book Description</button></li>
          </ul>
        </div>
        {detailsBody}
      </div>
    </main>
  );
}
