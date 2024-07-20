import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { industryList } from '../components/industrylist.jsx';


function Scores() {
    const endpoint = import.meta.env.VITE_MONGODB_ENDPOINT + "/action/find";
    const apiKey = import.meta.env.VITE_MONGODB_API_KEY;

    const [documents, setDocuments] = useState([]);
    
    const data = JSON.stringify({
        "collection": "companyScores",
        "database": "esgeepeetee_companies",
        "dataSource": "ESGeePeeTee",
    });

    const config = {
        method: 'post',
        url: endpoint,
        headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        },
        data: data,
    };

    useEffect(() => {
        axios(config)
        .then((response) => {
            // Access the array of documents directly from response.data
            setDocuments(response.data.documents)
            console.log(JSON.stringify(documents));
        })
        .catch((error) => {
            console.error(error);
        });
    }, [])
    
    return (
        <div id='Scores'>
          <div className='titleBar'>
              <h1 className='title'>All Analyzed Companies</h1>
          </div>
          <div id="companyList">
            {documents.map((document, index) => {
              const industry_label = industryList[document.industry];
              return (
                <div key={index} className="card">
                  <Link to='/DetailedScorePage' state={document}>
                    <h2>{document.company}</h2>
                  </Link>
                  <h3>{industry_label}</h3>
                  <h2>{document.total_score}</h2>
                </div>
            );})}
          </div>
          <div class='to-home'>
            <a href='/'><button class='home-button'>{'Back to Home'}</button></a>
          </div>
        </div>   
      ); 
};

export default Scores;