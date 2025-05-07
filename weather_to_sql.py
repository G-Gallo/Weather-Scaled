import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from weather_aggregation import cleaned_aggregated_dfs

#Create SQL Tables
Base = declarative_base()

#Database Credentials
USERNAME = "*******"
PASSWORD = "******"
HOST = "******"
DATABASE = "*******"

# Create Database Engine
engine = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}")

#Create Country DB
countries = [['Cairo', 'Egypt'], ['Delhi', 'India'], ['Karachi', 'Pakistan'], ['London', 'England'], ['Los Angeles', 'USA'],
             ['Mexico City', 'Mexico'], ['New York City', 'USA'], ['Seoul', 'South Korea'], ['Shanghai', 'China'], ['Tokyo', 'Japan']]
countries_db = pd.DataFrame(countries, columns=['City', 'Country'])
countries_db['ID'] = range(1, len(countries_db) + 1)
column_to_move = 'ID'
countries_db.insert(0, column_to_move, countries_db.pop(column_to_move))
print(countries_db)

#SQL DB Schemes
class Country(Base):
    __tablename__ = 'countries_db'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    City = Column(String, nullable=False)
    Country = Column(String, nullable=False)

class WeatherMonthly(Base):
    __tablename__ = 'weather_monthly'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    City_ID = Column(Integer, ForeignKey('countries_db.ID'), nullable=False)
    Date = Column(String, nullable=False)
    Average_Temp = Column(Float, nullable=False)
    Month = Column(String, nullable=False)
    Rain = Column(Float, nullable=False, default=0.0)
    Freezing_Rain = Column(Float, nullable=False, default=0.0)
    Snow = Column(Float, nullable=False, default=0.0)
    Rain_Snow = Column(Float, nullable=False, default=0.0)
    
    city = relationship("Country")

class WeatherDaily(Base):
    __tablename__ = 'weather_daily'
    
    ID = Column(Integer, primary_key=True, autoincrement=True)
    City_ID = Column(Integer, ForeignKey('countries_db.ID'), nullable=False)
    Date = Column(Date, nullable=False) 
    Average_Temp = Column(Float, nullable=False)

    city = relationship("Country")



#Upload Tables
def upload_to_mysql(df, table_name):
    if df is not None:
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f" Uploaded: {table_name}")

for country, data_dict in cleaned_aggregated_dfs.items():
    print(f"Uploading data for {country}...")
    
    country_table_prefix = country.lower().replace(" ", "_")

    upload_to_mysql(data_dict['monthly_average_temp'], f"{country_table_prefix}_monthly_avg_temp")
    upload_to_mysql(data_dict['daily_average_temp'], f"{country_table_prefix}_daily_avg_temp")
    upload_to_mysql(data_dict['precip_avg_monthly'], f"{country_table_prefix}_precip_avg_monthly")
    upload_to_mysql(data_dict['conditions_monthly_avg'], f"{country_table_prefix}_conditions_avg")

print("All data successfully uploaded to MySQL!")
