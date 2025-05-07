import pymysql

import pandas as pd

"""#Import MySQL Database
host = '127.0.0.2'
port = 3306
user = 'root'
password = 'GratCode1122'
database = 'weather_databases'

connection = pymysql.connect(host=host,
                             user=user,
                             port=port,
                             password=password,
                             database=database)

cursor = connection.cursor()

cursor.execute("SHOW TABLES")
tables = [table[0] for table in cursor.fetchall()]
country_dfs = {}
for table in tables:
    query = f"SELECT * FROM `{table}`" 
    country_dfs[table] = pd.read_sql(query, connection)

cursor.close()
connection.close()"""

#Test Data
file_path = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Raw_10_Country_Data.xlsx"
sheet_name = 'Raw_10_Country_Data'
df_dict = pd.read_excel(file_path, sheet_name=sheet_name)

country_dfs = {country: data for country, data in df_dict.groupby('name')}

#Clean and Aggregate Data
class clean_data:
    def __init__(self, df):
        self.df = df.copy()
    
    @staticmethod
    def _clean_data(df):
        df = df.drop(['name', 'description', 'icon', 'stations'], axis=1)
        df.rename(columns={'datetime': 'date'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        return df

class weather_aggregations:
    @staticmethod
    def temperature_agg(df, freq):
        avg = df[['temp']].resample(freq).mean().round(2)
        avg.reset_index(inplace=True)
        avg['Date'] = avg['date'].dt.strftime('%Y-%m')
        avg['Average'] = avg['temp']
        avg.drop(columns=['date', 'temp'], inplace=True)
        return avg[['Date', 'Average']]
    
    @staticmethod
    def monthly_avg_precipitation(df):
        precip_encoded = pd.get_dummies(df['preciptype'])
        precip_avg_monthly = precip_encoded.groupby(df.index.month).mean()
        precip_avg_monthly = (precip_avg_monthly * 100).round(2)
        precip_avg_monthly['month'] = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec']

        precipitation_mapping = {
        'rain': 'rain',
        'rfs': 'rfs', 
        'rain_snow': 'rain_snow',
        'snow': 'snow'}
    
        existing_cols = [col for col in precipitation_mapping.keys() 
                        if col in precip_encoded.columns]
        
        precip_avg_monthly = precip_avg_monthly.rename(
            columns={col: precipitation_mapping[col] for col in existing_cols}
        )
        
        final_cols = ['month'] + [col for col in precipitation_mapping.values() 
                                if col in precip_avg_monthly.columns]
        precip_avg_monthly = precip_avg_monthly[final_cols]

        precip_avg_monthly_melt = precip_avg_monthly.melt(id_vars='month', var_name='weather type', value_name='percentage')
        return precip_avg_monthly_melt, precip_encoded
    
    @staticmethod
    def all_precipitation_stats(df, precip_encoded):
        df["year_month"] = df.index.to_period("M")
        total_precip_num_monthly = precip_encoded.groupby(df["year_month"]).sum()
        
        rain_stats = rfs_stats = rain_snow_stats = snow_stats = None

        def calculate_stats(df, col_name):
            temp_df = df[[col_name]].copy()
            stats = (temp_df.groupby(temp_df.index.month).agg(['mean', 'min', 'max'])).round(2)
            stats.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            stats.reset_index(inplace=True)
            stats.columns = ['Month', 'Average', 'Min', 'Max']
            return stats

        if 'rain' in total_precip_num_monthly.columns:
            rain_stats = calculate_stats(total_precip_num_monthly, 'rain')
        
        if 'rain,freezingrain,snow' in total_precip_num_monthly.columns:
            rfs_stats = calculate_stats(total_precip_num_monthly, 'rain,freezingrain,snow')
        
        if 'rain,snow' in total_precip_num_monthly.columns:
            rain_snow_stats = calculate_stats(total_precip_num_monthly, 'rain,snow')
        
        if 'snow' in total_precip_num_monthly.columns:
            snow_stats = calculate_stats(total_precip_num_monthly, 'snow')
        
        return rain_stats, rfs_stats, rain_snow_stats, snow_stats
    
    @staticmethod
    def conditions(df):
        conditions_encoded = pd.get_dummies(df['conditions'])
        conditions_monthly_avg = conditions_encoded.groupby(df.index.month).mean()
        conditions_monthly_avg = (conditions_monthly_avg * 100).round(2)
        conditions_monthly_avg['month'] = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec']
        conditions_monthly_avg = conditions_monthly_avg.rename(columns={'Clear': 'clear',
                                                                        'Overcast': 'overcast',
                                                                        'Partially cloudy': 'partially_cloudy',
                                                                        'Rain': 'rain',
                                                                        'Rain, Overcast': 'rain_overcast',
                                                                        'Rain, Partially cloudy': 'rain_partially_cloudy',
                                                                        'Snow': 'snow',
                                                                        'Snow, Overcast': 'snow_overcast',
                                                                        'Snow, Partially cloudy': 'snow_partially_cloudy',
                                                                        'Snow, Rain': 'snow_rain',
                                                                        'Snow, Rain, Freezing Drizzle/Freezing Rain, Partially cloudy': 'snow_rain_fr_partially_cloudy',
                                                                        'Snow, Rain, Overcast': 'snow_rain_overcast',
                                                                        'Snow, Rain, Partially cloudy': 'snow_rain_partially_cloudy',
                                                                        'month': 'month'})
        conditions_monthly_avg = conditions_monthly_avg [['month'] + [col for col in conditions_monthly_avg.columns if col != 'month']]

        conditions_monthly_avg_melt = conditions_monthly_avg.melt(id_vars='month', var_name='condition', value_name='percentage')
        return conditions_monthly_avg_melt
    
#Loop through all countries and apply cleaning and aggregations
cleaned_aggregated_dfs = {}

for country, df in country_dfs.items():
    print(f"Processing data for {country}...")

    #Clean Data
    df_cleaned = clean_data._clean_data(df)

    #Aggregations
    monthly_temp = weather_aggregations.temperature_agg(df_cleaned, 'ME')
    daily_temp = weather_aggregations.temperature_agg(df_cleaned, 'D')
    precip_avg_monthly, precip_encoded = weather_aggregations.monthly_avg_precipitation(df_cleaned)
    rain_stats, rfs_stats, rain_snow_stats, snow_stats = weather_aggregations.all_precipitation_stats(df_cleaned, precip_encoded)
    conditions_monthly_avg = weather_aggregations.conditions(df_cleaned)

    #Store results in final structure
    cleaned_aggregated_dfs[country] = {
        'monthly_average_temp': monthly_temp,
        'daily_average_temp': daily_temp,
        'precip_avg_monthly': precip_avg_monthly,
        'rain_stats': rain_stats,
        'rfs_stats': rfs_stats,
        'rain_snow_stats': rain_snow_stats,
        'snow_stats': snow_stats,
        'conditions_monthly_avg': conditions_monthly_avg
    }

