import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function Home() {
  const [searchQuery, setSearchQuery] = useState(''); // Initialize searchQuery state

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  }

  const handleSearchClick = () => {
    event.preventDefault();
    console.log(searchQuery); // Log the current searchQuery on click
  }

  return (
    <>
      <div className='titleBar'>
        <h1 className='title'>ESGeePeeTee</h1>
      </div>
      <div id="searchBar">
        <form className="form">
          <input type='text' id='searchBox' class='inputBox' placeholder='Company Name' autoComplete='false' onChange={handleSearchChange} value={searchQuery} />
          <button id='searchBtn' onClick={handleSearchClick}>Search</button>
        </form>
      </div>
      <div id='actionsBar'>
        <Link to='/Scores'><button>View List</button></Link>
        <Link to='/Add'><button>Add New</button></Link>
        <Link to='/DetailedScorePage'><button>Test DSP</button></Link>
      </div>
    </>
  )
}

export default Home;
