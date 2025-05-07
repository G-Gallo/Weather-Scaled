import requests
import sys
import pandas as pd
import csv
import codecs
        

response = requests.request("GET", "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Tokyo/2024-01-01/2025-01-01?unitGroup=us&include=hours&key=V29UE9AMYM6D62AS4CKTZHGCP&contentType=csv")
if response.status_code!=200:
  print('Unexpected Status code: ', response.status_code)
  sys.exit()  


# Parse the results as CSV
CSVText = csv.reader(response.text.splitlines(), delimiter=',',quotechar='"')
data = list(CSVText)
df = pd.DataFrame(data[1:], columns=data[0])

#Upload to MySQL
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#Create SQL Tables
Base = declarative_base()

#Database Credentials
USERNAME = "root"
PASSWORD = "GratCode1122"
HOST = "127.0.0.2:3306"
DATABASE = "world_weather_raw"

#Create Database Engine
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

#Upload Raw Data
df.to_sql('raw_data', con=engine, if_exists='replace', index=False)