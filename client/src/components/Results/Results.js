import React from 'react';
import Result from './Result/Result';

import "./Results.css";

export default function Results(props) {
  //console.log(props);

  const queryType = props.queryType;
  console.log("Query Type: "+queryType);
  let results = props.documents.map((result, index) => {
    return <Result 
        key={index} 
        document={result}
      />;
  });

  let beginDocNumber = Math.min(props.skip + 1, props.count);
  let endDocNumber = Math.min(props.skip + props.top, props.count);
  if (queryType === 'normal') { 
  return (
    <div>
      <p className="results-info">Showing {beginDocNumber}-{endDocNumber} of {props.count.toLocaleString()} results</p>
      <div className="row row-cols-md-5 results">
        {results}
      </div>
    </div>
  );
  } else {

    return (
      <div>
        <p></p>
        <div className="row row-cols-md-5 results">
          {results}
        </div>
      </div>
    );
  }

};
