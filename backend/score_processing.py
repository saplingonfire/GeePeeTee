import requests
import pandas as pd
from datetime import datetime

def process_tones(weight_arr):
    normalized_tones = [0 if w <-0.5 else 60 if w <3.5 else 100 for w in weight_arr]
    return sum(normalized_tones)/len(normalized_tones)

def score_question(company, keywords):
    # Define the API endpoint URL
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    # Set parameters
    params = {
        "query": f"{company} ({' OR '.join(keywords.split(' '))})",
        "mode": "timelinetone",
        "format": "json",
        "timespan": "12m",
    }

    # Send GET request with parameters
    response = requests.get(url, params=params)
    response_data = response.json()['timeline'][0]['data']
    # print(response_data)
    weight_array = [sample['value'] for sample in response_data]
    avg = process_tones(weight_array)
    print(f"Search for {company} with keywords: ({keywords}) scored {avg} points")
    return avg

def score_company(company, industry): 

    component_scores={}
    #Remember to change the file directory 
    industry_df = pd.read_excel('./csa_weights_final.xlsx', sheet_name=industry, header=0)
    keywords_df = pd.read_excel('./csa_weights_final.xlsx', sheet_name='CRITERIA', header=0)
    keywords_dict = {row['Criteria']: row['Keywords'] for index, row in keywords_df.iterrows()}

    for index, row in industry_df.iterrows():
        criteria = row['Criteria']
        cweight = row['Criteria Weight']
        keywords = criteria + " " + keywords_dict[criteria]
        dimension = row['Dimension']
        # print(criteria, cweight)
        try:
            question_points = score_question(company, keywords)
        except:
            # No contribution to ESG score if there is no relevant data
            question_points = 0
        esgScore = cweight * question_points/100
        if dimension not in component_scores:
            component_scores[dimension]=[esgScore,cweight]
        else:
            component_scores[dimension][0]+=esgScore
            component_scores[dimension][1]+=cweight

    for v in component_scores.values():
        v[0]=round(v[0])

    data={
        'company':company,
        'industry':industry,
        'total_score':sum(values[0] for values in component_scores.values()),
        'environmental':{'score':component_scores['Environmental'][0], 'dimension_total':component_scores['Environmental'][1]},
        'social':{'score':component_scores['Social'][0], 'dimension_total':component_scores['Social'][1]},
        'governance':{'score':component_scores['Governance'][0], 'dimension_total':component_scores['Governance'][1]},
        'timestamp':datetime.today().strftime('%Y-%m-%d')
    }
    # print(f"ESG score: {sum(values[0] for values in component_scores.values())}")
    # print(component_scores)
    # print(f'ESG Risk Rating: {round(100-esgScore)}')
    return data

##########################################################################
    #INPUT#
##########################################################################
# score_company('Apple Inc', "THQ")
