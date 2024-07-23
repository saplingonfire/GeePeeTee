import React from 'react';

export async function ReloadScore(companyName, companyIndustry) {
    const backendEndpoint = import.meta.env.VITE_BACKEND_ENDPOINT;
    const apiPath = backendEndpoint + '/api/receive_json';

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
    console.log(data);
    
}

