import { industryList } from '../components/industrylist.jsx';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

function Add() {
    const [isLoading, setIsLoading] = useState(false);
    const backendEndpoint = import.meta.env.VITE_BACKEND_ENDPOINT;
    const apiPath = backendEndpoint + '/api/receive_json';
    const navigate = useNavigate();

    const populateIndustries = () => {
        return Object.entries(industryList).map(([code, industry]) => (
          <option value={code} key={code}>{industry}</option>
        ));
    };      

    const handleAddCompany = async() => {
        event.preventDefault();
        setIsLoading(true);
        const companyName = document.getElementById('addCompanyInput').value;
        const companyIndustry = document.getElementById('selectIndustry').value;
        if (!companyName) {
            console.error('Company name input field is missing');
            return;
        }
        if (companyIndustry === 'default') {
            console.error('Industry selection is missing');
            return;
        }

        const response = await fetch(apiPath, {
            method: 'POST',
            body: JSON.stringify({
              company: companyName,
              industry: companyIndustry,
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8",
              'Access-Control-Allow-Origin': '*'
            }
        });
          
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        setIsLoading(false);
        navigate('/DetailedScorePage', {state: data});
        // console.log(data);
    };

    return (
        <>
            <div className='titlebar'>
                <h1 className="title">Analyze New Company</h1>            
            </div>
            <div id="addCompanyBar">
                <form className="form">
                    <input type="text" className='inputBox' id='addCompanyInput' placeholder="Company Name" autoComplete='false'/>
                    <select id='selectIndustry' className='inputBox' autoComplete="true" defaultValue='default'>
                        <option value='default' disabled>Select an Industry</option>
                        {populateIndustries()}
                    </select>
                    <button id='addBtn' onClick={handleAddCompany}>Add to Queue</button>
                </form>
            </div>
            <div>
                <a href='/' id='add-to-home'><button class='home-button'>{'Back to Home'}</button></a>
            </div>
            {isLoading && 
                <div id='loading-box'>
                    <h1>Please wait for analysis to be complete</h1>
                    <img id='loading-wheel' src="/src/assets/loading.gif"/>
                </div>
            }
        </> 
    )
};

export default Add;