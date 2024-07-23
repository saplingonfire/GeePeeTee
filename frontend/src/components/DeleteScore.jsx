import axios from "axios";

export function DeleteScore(companyName) {
    const endpoint = import.meta.env.VITE_MONGODB_ENDPOINT + "/action/deleteOne";
    const apiKey = import.meta.env.VITE_MONGODB_API_KEY;
    const data = JSON.stringify({
        "collection": "companyScores",
        "database": "esgeepeetee_companies",
        "dataSource": "ESGeePeeTee",
        "filter": {
            "company": companyName,
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
        if (response.statusCode === 200) {
            console.log(`${companyName}'s ESG score successfully deleted`);
        }
    })
    .catch((error) => {
        console.error(error);
    });
}