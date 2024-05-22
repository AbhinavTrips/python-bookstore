import React, {useState} from 'react';

import "./SearchBar.css";

export default function SearchBar(props) {

    let [q, setQ] = useState("");


    const onSearchHandler = () => {
        props.postSearchHandler(q);
    }



    const onEnterButton = (event) => {
        if (event.keyCode === 13) {
            onSearchHandler();
        }
    }

    const onChangeHandler = () => {
        var searchTerm = document.getElementById("search-box").value;
        setQ(searchTerm);

        // use this prop if you want to make the search more reactive
        if (props.searchChangeHandler) {
            props.searchChangeHandler(searchTerm);
        }
    }


    return (
        <div >
            <div  className="input-group stack align-right" onKeyDown={e => onEnterButton(e)}>
                <div className="margin" >
                    <textarea
                        autoComplete="off" // setting for browsers; not the app
                        type="text" 
                        id="search-box" 
                        className="form-control rounded-0" 
                        placeholder="Ask a question about kind of books that you wanna read to get relevant results. OR leave it blank to get all books." 
                        onChange={onChangeHandler} 
                        defaultValue={props.q} >
                    </textarea>
                </div>
                <div className="input-group-btn right-align">
                    <button className=" btn btn-primary rounded-0" type="submit" onClick={onSearchHandler}>
                        Search
                    </button>
                </div>
            </div>
        </div>
    );
};