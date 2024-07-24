from data_function import esg_dimension
from data_function import dimension_tone_data
import pandas as pd
import numpy as np
import json

company_data={"Singapore Airlines":"AIR", 
                'Apple Inc':"THQ", 
                'Microsoft':"SOF",
                "Tesla":"AUT", 
                "Alphabet":"IMS",
            "Meta Platforms":"IMS", 
                "The Coca Cola Company":"BVG", 
            "NVIDIA":"SEM", 
                "Visa Inc":"FBN",
               "Intel Corporation":"SEM",
               "Nike":"TEX",
               "McDonald's":"REX",
                "Adobe":"SOF",
                "Starbucks":"REX",
             "Target Corporation":"FDR",
             "Pfizer":"DRG",
             "Amgen":"BTC",
             "Caterpillar":"IEQ",
             "Lockheed Martin":"ARO",
             "Schlumberger":"OIE",
             "Exelon":"ELC",
             "Dominion Energy":"MUW",
             "Comcast":"PUB",
                "Oracle":"SOF",
                'Walt Disney':"PUB",
                "Ford Motor":"AUT",
                "American Express":"FBN",
                "Berkshire Hathaway":"FBN",
                "BlackRock":"FBN",
                "Medtronic":"MTC",
                "Kraft Heinz":"FOA",
                "Boeing":"ARO",
                "American Airlines":"AIR",
                "United Airlines":"AIR",
                "Aluminium Corporation of China":"ALU",
                "JBM Auto":"ATX",
                "Summit Materials":"BLD",
                "United Overseas Bank Limited":"BNK",
                "Tata Chemicals":"CHM",
                "Motorola":"CMT",
                "Las Vegas Sands":"CNO",
                "Peabody Energy":"COL",
                "Martin Marietta Materials":"COM",
                "EMCOR Group":"CON",
                "Gillette":"COS",
                "Graham Holdings":"CSV",
                "Amcor":"CTR",
                "Tempur Sealy International":"DHP",
                "Powell Industries":"ELQ",
                "Asia Paper Manufacturing":"FRP",
               }


companies = dimension_tone_data(company_data)
print("Tone data done")
print()

esg_df = esg_dimension(company_data)
print("ESG data done")
print()

def load_dimension_data(dimension_list,companies):
    for dimension in dimension_list:
        filtered = {}
        for c in companies[dimension]:
            tone_string =  json.dumps(companies[dimension][c])
            filtered[c] = tone_string
        dimensiontone_df = pd.DataFrame(list(filtered.items()), columns=['company', 'Tone_Array'])
        train_df = pd.merge(esg_df[['company','Sector',f'{dimension}_Score']],dimensiontone_df,on='company',how='inner')
        train_df.to_excel(f'{dimension}_esg_tone.xlsx',index=False)
        print(f"Environmental DataFrame has been saved to '{dimension}_esg_tone.xlsx'")

dimension_list = ['Environmental','Social','Governance']
dimension_list2 = ['Environmental']
load_dimension_data(dimension_list,companies)




