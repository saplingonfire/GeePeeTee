import requests
import json

endpoint_url = " https://ap-southeast-1.aws.data.mongodb-api.com/app/data-fevcdnd/endpoint/data/v1/action" #edit your endpoint
API_KEY = 'KdrhLZMfd335dURL2AUB2Tbtav6SCdtCBdbyrBRX1OwFHzd2H4rEtG1YKzgtD8o9'

filter_url = f'{endpoint_url}/findOne'
update_url = f'{endpoint_url}/updateOne'
insert_url = f'{endpoint_url}/insertOne'

def store_or_update_esg_scores(company_data):
    headers = {
        'Content-Type': 'application/json',
        'api-key': API_KEY
    }

    filter_query = {
        "dataSource": "ESGeePeeTee",
        "database": "esgeepeetee_companies",
        "collection": "companyScores",
        "filter": {"company": company_data['company']}
    }

    update_query = {
        "dataSource": "ESGeePeeTee",
        "database": "esgeepeetee_companies",
        "collection": "companyScores",
        "filter": {"company": company_data['company']},
        "update": {"$set": {
            "industry": company_data["industry"],
            "total_score": company_data["total_score"],
            "environmental": company_data["environmental"],
            "social": company_data["social"],
            "governance": company_data["governance"],
            "timestamp": company_data["timestamp"]
        }}
    }

    insert_query = {
                "dataSource": "ESGeePeeTee",
                "database": "esgeepeetee_companies",
                "collection": "companyScores",
                "document": company_data
                }

    try:
        # Check if the company exists
        response = requests.post(filter_url, headers=headers, json=filter_query)
        response_data = response.json()

        if response.status_code == 200:
            if response_data.get('document'):  # Company exists, update it
                update_response = requests.post(update_url, headers=headers, json=update_query)
                if update_response.status_code == 200:
                    print(f"Successfully updated ESG scores for {company_data['company']}.")
                else:
                    print(f"Failed to update ESG scores for {company_data['company']}.")
            else:  # Company does not exist, insert new document
                insert_response = requests.post(insert_url, headers=headers, json=insert_query)
                print(insert_response.status_code)
                if insert_response.status_code == 201:
                    print(f"Successfully inserted new ESG scores for {company_data['company']}.")
                else:
                    print(f"Failed to insert new ESG scores for {company_data['company']}.")
        else:
            print(f"Failed to query MongoDB. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    print("----------------------")

if __name__ == "__main__":
    # Example company data to update or store
    company_data = {'company': 'Boeing', 
                    'industry': 'AIR', 
                    'total_score': 22, 
                    'environmental': {'score': 8, 'dimension_total': 35}, 
                    'social': {'score': 8, 'dimension_total': 37}, 
                    'governance': {'score': 6, 'dimension_total': 28}, 
                    'timestamp': '2024-07-22'}

    store_or_update_esg_scores(company_data)
