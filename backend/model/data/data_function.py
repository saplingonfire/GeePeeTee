import requests
import matplotlib.pyplot as plt
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import seaborn as sns
import re
from bs4 import BeautifulSoup

#get tone analysis
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

#get total tone from gdelt
def total_score_company(company, industry): 

    total_tone =[]
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
            question_points = score_question(company, keywords)
        except:
            # No contribution to ESG score if there is no relevant data
            question_points = []
            
        esgScore = (cweight * np.array(question_points)).tolist()
        total_tone += esgScore
        
    data={
        'company':company,
        'tones':total_tone
    }
    return data

#get dimension tones
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
            question_points = score_question(company, keywords)
        except:
            # No contribution to ESG score if there is no relevant data
            question_points = []
        
        if dimension not in total_tone:
            total_tone[dimension] = [(keywords,cweight,question_points)]
        else:
            total_tone[dimension] += [(keywords,cweight,question_points)]
        
    data={
        'company':company,
        'Environmental':total_tone['Environmental'],
        'Social':total_tone['Social'],
        'Governance':total_tone['Governance']
    }
    return data

#get total esg score from web
def esg_actual(company_data):
    driver = webdriver.Chrome()  # Make sure you have the correct driver installed

    # URL of the website
    url = "https://www.spglobal.com/esg/scores/results?cid=4023623"

    # Data collection
    data = []

    for company,sector in company_data.items():
        print(f"Finding ESG Score for {company}")
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='banner-search__input']"))
        )

        input_field.clear()
        input_field.send_keys(company)
        input_field.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for the results to load

        # Extract the information (example: company information)
        try:
            info = driver.find_element(By.CLASS_NAME, "scoreModule__score").text
            # Append the information to the data list
            print(f"ESG Score found for {company}")
            data.append([company, sector, info])
        except:
            print(f"{company} info not available.")

    # Close the WebDriver
    driver.quit()

    # Convert the data to a DataFrame
    esg_df = pd.DataFrame(data, columns=["company", "Sector","Score"])
    
    return esg_df

#process total tone
def total_tone_data(company_data):
    dataset = {}
    count = 1
    for companies in company_data:
        sector = company_data[companies]
        print(f"Loading tone for {companies}")
        tone_outcome = total_score_company(companies,sector)
        dataset[companies] = tone_outcome['tones']
        print(f"No {count}: Tone loaded for {companies}")
        count += 1
        
    return dataset

#get dimension tone from gdelt
def dimension_tone_data(company_data):
    dataset = {}
    count = 1
    for companies in company_data:
        sector = company_data[companies]
        print(f"Loading tone for {companies}")
        tone_outcome = dimension_score_company(companies,sector)
        if dataset:
            dataset['Environmental'][companies] = tone_outcome['Environmental']
            dataset['Social'][companies] = tone_outcome['Social']
            dataset['Governance'][companies] = tone_outcome['Governance']
        else:
            dataset['Environmental'] = {companies:tone_outcome['Environmental']}
            dataset['Social'] = {companies:tone_outcome['Social']}
            dataset['Governance'] = {companies:tone_outcome['Governance']}
        print(f"No {count}: Tone loaded for {companies}")
        count += 1
        
    return dataset

#process dimension score
def process_list_items(list_items):
    for item in list_items:
                html_content = item.get_attribute('innerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')

                span_element = soup.find('span')
                if span_element:
                    value_text = span_element.text.strip()
                    try:
                        numeric_value = float(value_text)
                        return numeric_value  # Do something with the extracted value
                    except ValueError:
                        print(f"Error converting value to numeric: {value}")
                else:
                    print("Span element not found")

                    span_element = soup.find('span')
                    if span_element:
                        value_text = span_element.text.strip()
                        try:
                            value = float(value_text)
                            print(value)  # Output: 90
                        except ValueError:
                            print("Error converting value to numeric:", value)
                    else:
                        print("Span element not found")

#get dimension scores from web
def esg_dimension(company_data):

    driver = webdriver.Chrome()  # Make sure you have the correct driver installed

    # URL of the website
    url = "https://www.spglobal.com/esg/scores/results?cid=4023623"

    # Data collection
    data = []

    for company,sector in company_data.items():
        print(f"Finding ESG Score for {company}")
        driver.get(url)
        time.sleep(3)  # Wait for the page to load
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='banner-search__input']"))
        )

        input_field.clear()
        input_field.send_keys(company)
        input_field.send_keys(Keys.RETURN)

        time.sleep(3)  # Wait for the results to load

        output = []
        # Extract the information (example: company information)
        try:
            

            #environmental 
            parent_element = driver.find_element(By.CLASS_NAME, 'dimention-chart1')
            list_items1 = parent_element.find_elements(By.CLASS_NAME, 'DimensionScore__label')
            dimension_score1 = process_list_items(list_items1)

            #Social
            parent_element = driver.find_element(By.CLASS_NAME, 'dimention-chart2')
            list_items2 = parent_element.find_elements(By.CLASS_NAME, 'DimensionScore__label')
            dimension_score2 = process_list_items(list_items2)

            #Governance
            parent_element = driver.find_element(By.CLASS_NAME, 'dimention-chart3')
            list_items3 = parent_element.find_elements(By.CLASS_NAME, 'DimensionScore__label')
            dimension_score3 = process_list_items(list_items3)

            data.append([company, sector, dimension_score1,dimension_score2,dimension_score3])

            
        except:
            print(f"{company} info not available.")

    # Close the WebDriver
    driver.quit()

    # Convert the data to a DataFrame
    esg_df = pd.DataFrame(data, columns=["company", "Sector","Environmental_Score","Social_Score","Governance_Score"])
    
    return esg_df




