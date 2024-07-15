import { industryList } from '../components/industrylist.jsx';

function Add() {
    
    const backendEndpoint = import.meta.env.VITE_BACKEND_ENDPOINT;

    const populateIndustries = () => {
        return Object.entries(industryList).map(([industry, code]) => (
          <option value={code} key={code}>{industry}</option>
        ));
    };      

    const handleAddCompany = async() => {
        event.preventDefault();
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

        const response = await fetch(backendEndpoint, {
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
        console.log(data.json);
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
        </> 
    )
};

export default Add;