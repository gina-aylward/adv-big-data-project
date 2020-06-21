import json
import os
import pandas as pd
import numpy as np

for file in os.listdir("out"):
    if file.endswith(".json"):
        data = pd.read_json('./out/' + file, orient='split')
        data.rename(columns={'Full Description':'full_description','Agent Address':'agent_address','Agent Name':'agent_name'}, inplace=True)
        
        data['number_bedrooms'] = pd.to_numeric(data['number_bedrooms'],errors='coerce')
        data = data.replace(np.nan, 0, regex=True)
        data['number_bedrooms'] = data['number_bedrooms'].astype(int)
        
        data['retirement'] = pd.to_numeric(data['retirement'],errors='coerce')
        data = data.replace(np.nan, 0, regex=True)
        data['retirement'] = data['retirement'].astype(int)
        
        data['agent_url'] = data['agent_url'].astype(str)
        data['viewType'] = data['viewType'].astype(str)
        data.viewType = data.viewType.replace({"0.0": "0"})
        mask = data.applymap(type) != bool
        d = {True: 'TRUE', False: 'FALSE'}

        data = data.where(mask, data.replace(d))

        print(os.path.basename(file))
        data.to_json('./json/' + file, orient='records', lines=True)
