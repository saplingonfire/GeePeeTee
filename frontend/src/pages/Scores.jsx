import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { industryList } from '../components/industrylist.jsx';
import { DeleteScore } from '../components/DeleteScore.jsx';
import { ReloadScore } from '../components/ReloadScore.jsx';

function Scores() {
    const [isLoading, setIsLoading] = useState(false);
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

    const handleDelete = (companyName) => {
      DeleteScore(companyName);
      location.reload();
    };
    
    const handleReload = async (companyName, industry) => {
      setIsLoading(true);
      await ReloadScore(companyName, industry);
      setIsLoading(false);
      location.reload();
    };

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
                  <h2>{industry_label}</h2>
                  <h2>{document.total_score}</h2>
                  <div className='card-company-actions'>
                    <button className='transparent' onClick={() => handleReload(document.company, document.industry)}><img className='small-icon' src="./src/assets/refresh.png"/></button>
                    <button className='transparent' onClick={() => handleDelete(document.company)}><img className='small-icon' src="./src/assets/delete.png"/></button>
                  </div>
                </div>
            );})}
          </div>
          <div class='to-home'>
            <a href='/'><button class='home-button'>{'Back to Home'}</button></a>
          </div>
          {isLoading && 
            <div id='loading-box'>
            <h1>{`Reloading score...`}</h1>
            <img id='loading-wheel' src="/src/assets/loading.gif"/>
            </div>
          }
        </div>
           
      ); 
};

export default Scores;