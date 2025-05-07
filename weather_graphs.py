from matplotlib import pyplot as plt
import seaborn as sns
import os
from weather_aggregation import cleaned_aggregated_dfs

#Output Folders
output_folder1 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\quarterly temperature"
output_folder2 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\precipitation by month"
output_folder3 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\rain stats"
output_folder4 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\rfs stats"
output_folder5 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\rain_snow stats"
output_folder6 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\snow stats"
output_folder7 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\conditions"
output_folder8 = "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\Graphs\\temperature box plot"


#Quarterly Temperature Graphs
for country, data in cleaned_aggregated_dfs.items():
    temp_data = data['daily_average_temp']

    plt.figure(figsize=(14, 7))
    sns.lineplot(data=temp_data, x='Date', y='Average')
    plt.title(f'All Time Monthly Average Temperature (F)\n {country}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (F)')
    plt.tight_layout()

    image_path = os.path.join(output_folder1, f"{country}_temperature.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Precipiation Chance by Month
for country, data in cleaned_aggregated_dfs.items():
    precip_chance = data['precip_avg_monthly']

    plt.figure(figsize=(14,7))
    sns.lineplot(data=precip_chance, x='month', y='percentage', hue='weather type')
    plt.title(f'Percent Precipitation By Month\n {country}')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.legend(title='Precipitation Type')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder2, f"{country}_percip_chances.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Rain Monthly Averages
for country, data in cleaned_aggregated_dfs.items():
    rain_stats = data['rain_stats']

    if rain_stats is None:
        print(f"Skipping rain stats for {country} - no data available")
        continue

    plt.figure(figsize=(14,7))
    sns.lineplot(data=rain_stats, x=rain_stats['Month'], y='Average')
    plt.fill_between(rain_stats['Month'], rain_stats['Min'], rain_stats['Max'], color='b', alpha=0.2)
    plt.title(f'Number of Rain Days by Month\n {country}')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder3, f"{country}_rain_stats.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Rain/Freezing_Rain/Snow
for country, data in cleaned_aggregated_dfs.items():
    rfs_stats = data['rfs_stats']

    if rfs_stats is None:
        print(f"Skipping rain/freezingrain/snow stats for {country} - no data available")
        continue

    plt.figure(figsize=(14,7))
    sns.lineplot(data=rfs_stats, x=rfs_stats['Month'], y='Average')
    plt.fill_between(rfs_stats['Month'], rfs_stats['Min'], rfs_stats['Max'], color='b', alpha=0.2)
    plt.title(f'Number of Rain,Freezing Rain, Snow Days by Month\n {country}')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder4, f"{country}_rfs_stats.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Rain/Snow Stats
for country, data in cleaned_aggregated_dfs.items():
    rain_snow_stats = data['rain_snow_stats']

    if rain_snow_stats is None:
        print(f"Skipping rain/snow stats for {country} - no data available")
        continue

    plt.figure(figsize=(14,7))
    sns.lineplot(data=rain_snow_stats, x=rain_snow_stats['Month'], y='Average')
    plt.fill_between(rain_snow_stats['Month'], rain_snow_stats['Min'], rain_snow_stats['Max'], color='b', alpha=0.2)
    plt.title(f'Number of Rain/Snow Days by Month\n {country}')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder5, f"{country}_rain_snow_stats.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Snow Stats
for country, data in cleaned_aggregated_dfs.items():
    snow_stats = data['snow_stats']

    if snow_stats is None:
        print(f"Skipping snow stats for {country} - no data available")
        continue

    plt.figure(figsize=(14,7))
    sns.lineplot(data=snow_stats, x=snow_stats['Month'], y='Average')
    plt.fill_between(snow_stats['Month'], snow_stats['Min'], snow_stats['Max'], color='b', alpha=0.2)
    plt.title(f'Number of Snow Days by Month\n {country}')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder6, f"{country}_snow_stats.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Monthly Conditions
for country, data in cleaned_aggregated_dfs.items():
    conditions_monthly_avg_melt = data['conditions_monthly_avg']

    plt.figure(figsize=(14,7))
    sns.lineplot(data=conditions_monthly_avg_melt, x='month', y='percentage', hue='condition', palette="tab10")
    plt.title('Percent Condition By Month\n Seoul, South Korea')
    plt.xlabel('Month')
    plt.ylabel('Percentage')
    plt.legend(title='Condition', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder7, f"{country}_conditions.png")
    plt.savefig(image_path, dpi=300)
    plt.close()

#Monthly Temperature Box Plot
for country, data in cleaned_aggregated_dfs.items():
    temp_data = data['monthly_average_temp']

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=temp_data, x=temp_data['Date'], y='Average', palette="tab10")
    plt.title(f'Monthly Temperature(F)\n {country}')
    plt.xlabel('Date')
    plt.ylabel('Temperature (F)')
    plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    image_path = os.path.join(output_folder8, f"{country}_temp_boxplot.png")
    plt.savefig(image_path, dpi=300)
    plt.close()