import React from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Home() {

  const endpoint = import.meta.env.VITE_MONGODB_ENDPOINT + "/action/findOne";
  const apiKey = import.meta.env.VITE_MONGODB_API_KEY;
  const navigate = useNavigate();

  const handleSearchClick = () => {
    event.preventDefault();
    const searchCompany = document.getElementById('searchBox').value;

    const data = JSON.stringify({
      "collection": "companyScores",
      "database": "esgeepeetee_companies",
      "dataSource": "ESGeePeeTee",
      "filter": {
        "company": searchCompany,
      },
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

    axios(config)
    .then((response) => {
        // Access the array of documents directly from response.data
        if (response.data.document !== null) {
          navigate('/DetailedScorePage', {state: response.data.document});
        } else {
          alert("Couldn't find company. Have you entered the right name?");
        }
    })
    .catch((error) => {
        console.error(error);
    });
  }

  return (
    <>
      <div className='titleBar'>
        <h1 className='title'>ESGeePeeTee</h1>
      </div>
      <div id="searchBar">
        <form className="form">
          <input type='text' id='searchBox' autoComplete='off' className='inputBox' placeholder='Company Name' />
          <button id='searchBtn' onClick={handleSearchClick}>Search</button>
        </form>
      </div>
      <div id='actionsBar'>
        <Link to='/Scores'><button>View List</button></Link>
        <Link to='/Add'><button>Add New</button></Link>
      </div>
    </>
  )
}

export default Home;
