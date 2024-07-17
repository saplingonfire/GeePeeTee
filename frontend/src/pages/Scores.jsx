import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Scores() {
    const endpoint = import.meta.env.VITE_MONGODB_ENDPOINT;
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
            console.log(document)
            return (
            <div key={index} className="card">
              <h2>{document.data.company}</h2>
              <h3>{document.data.industry}</h3>
              <h2>{document.data.total_score}</h2>
            </div>
          );})}
        </div>
        </div>   
      ); 
};

export default Scores;