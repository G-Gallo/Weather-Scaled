import subprocess

scripts = [
    "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\weather_aggregation.py",
    "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\weather_graphs.py",
    "C:\\Users\\garre\\OneDrive\\Desktop\\Coding\\Port_Project\\Korea Weather\\Weather_Scaled\\weather_to_sql.py"
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script])
    print(f"Finished {script}!\n")