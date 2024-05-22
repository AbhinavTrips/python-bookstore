import React from 'react';

import './Result.css';

export default function Result(props) {
    
    console.log(`result prop = ${JSON.stringify(props)}`)
    
    return(
    <div className="card result">
        <a href={`/details/${props.document.id}/${props.document.isbn10}`}>
            <img className="card-img-top" src={props.document.thumbnail} alt={props.document.title}></img>
            <div className="card-body">
                <h6 className="title-style">{props.document.title}</h6>
            </div>
        </a>
    </div>
    );
}
