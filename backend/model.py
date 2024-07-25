from sklearn.model_selection import train_test_split
from autogluon.tabular import TabularDataset, TabularPredictor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import requests
from datetime import datetime
import json

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
    return weight_array

def dimension_score_company(company, industry): 

    total_tone ={}
    #Remember to change the file directory 
    industry_df = pd.read_excel('./csa_weights_final.xlsx', sheet_name=industry, header=0)
    keywords_df = pd.read_excel('./csa_weights_final.xlsx', sheet_name='CRITERIA', header=0)
    keywords_dict = {row['Criteria']: row['Keywords'] for index, row in keywords_df.iterrows()}

    for index, row in industry_df.iterrows():
        criteria = row['Criteria']
        cweight = row['Criteria Weight']
        keywords = criteria + " " + keywords_dict[criteria]
        dimension = row['Dimension']
#         print(keywords, cweight)
        try:
            print(f"Extracting tone of keyword {keywords} for {company}")
            question_points = score_question(company, keywords)
        except:
            question_points = []

        if dimension not in total_tone:
            total_tone[dimension] = [(keywords,cweight,question_points)]
        else:
            total_tone[dimension] += [(keywords,cweight,question_points)]

    print("Tone Extraction Done")
    print("----------------------")
    data={
        'company':company,
        'industry':industry,
        'Environmental':total_tone['Environmental'],
        'Social':total_tone['Social'],
        'Governance':total_tone['Governance']
    }
    return data

def model(dimension,data):
    spredictor = TabularPredictor.load("model/S/AutogluonModels/ag-20240725_072405")
    gpredictor = TabularPredictor.load("model/G/AutogluonModels/ag-20240724_085946")
    epredictor = TabularPredictor.load("model/E/AutogluonModels/ag-20240725_071642")

    if dimension == 'Environmental':
        predictor = epredictor
    elif dimension == 'Social':
        predictor =  spredictor
    else:
        predictor = gpredictor


    start_time = time.time()
    new_predictions = predictor.predict(data)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # print(f"Prediction time: {elapsed_time:.4f} seconds")
    # print()
    # print(f"Prediction for {dimension} is",new_predictions.iloc[0])

    return(new_predictions.iloc[0])

def get_prediction(data):

    escore = 0
    for score in data['Environmental']:
        escore += score[1]
    etones_string = json.dumps(data['Environmental'])
    environmental_df = pd.DataFrame({'company': data['company'],'Sector': data['industry'],'Tone_Array': etones_string}, index=[0])
    environment_score = model("Environmental",environmental_df)
    print("Environmental Model Prediction Done")
    
    sscore = 0
    for score in data['Social']:
        sscore += score[1]
    stones_string = json.dumps(data['Social'])
    social_df = pd.DataFrame({'company': data['company'],'Sector': data['industry'],'Tone_Array': stones_string}, index=[0])
    social_score = model("Social",social_df)
    print("Social Model Prediction Done")
    
    
    gscore = 0
    for score in data['Governance']:
        gscore += score[1]
    gtones_string = json.dumps(data['Governance'])
    governance_df = pd.DataFrame({'company': data['company'],'Sector': data['industry'],'Tone_Array': gtones_string}, index=[0])
    governance_score = model("Governance",governance_df)
    print("Goverance Model Prediction Done")
    
    
    
    total_score = (environment_score/100) * escore + (social_score/100) * sscore + (governance_score/100) * gscore

    output = {
        'company':data['company'],
        'industry':data['industry'],
        'total_score':round(total_score,0),
        'environmental':{'score': round((environment_score/100) * escore,0) , 'dimension_total': escore},
        'social':{'score': round((social_score/100) * sscore,0) , 'dimension_total': sscore},
        'governance':{'score': round((governance_score/100) * gscore,0) , 'dimension_total': gscore},
        'timestamp':datetime.today().strftime('%Y-%m-%d')
    }


    return output

if __name__ == "__main__":
    def testing(test_list):
        for item in test_list:
            start_time = start_time = time.time()
            company = item
            sector = test_list[item]
            print(f"Starting Analysis for {company} in {sector}")
            data = dimension_score_company(company, sector)
            outcome = get_prediction(data)
            print(outcome)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Analysis took: {elapsed_time:.4f} seconds")
            print("--------------------------")

    test_list = {"Nomura Holdings": "FBN",
    "NVIDIA":"SEM",
    "Novartis":"DRG",
    "Apple Inc":"THQ",
    "Adobe Inc": "SOF",
    "Toyota Motor Corporation":"AUT",
    "Tesla Inc":"AUT"}

    testing(test_list)
