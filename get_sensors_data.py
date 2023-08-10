import subprocess
import re
import time
import csv
import json
from datetime import datetime

command = 'sensors -j'
# CSV file to store data
csv_file = 'sensors_data.csv'
with open(csv_file, 'a', newline='') as file:
    writer = csv.writer(file)
    header_flag =True
# Main loop to run the sensors command every two seconds and store data in CSV file
    for _ in range(325):
        output = subprocess.run(command, shell=True, text=True, capture_output=True)
        data=output.stdout
        parsed_data = json.loads(data)
        print(parsed_data["apm_xgene-isa-0000"])
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        SoC_Temperature=parsed_data["apm_xgene-isa-0000"]["SoC Temperature"]["temp1_input"]
        CPU_Power=parsed_data["apm_xgene-isa-0000"]["CPU power"]["power1_input"]
        IO_Power=parsed_data["apm_xgene-isa-0000"]["IO power"]["power2_input"]
        if header_flag:
            writer.writerow(['Timestamp','SoC Temperature (°C)','CPU Power (W)','IO Power (W)'])
        writer.writerow([current_time,SoC_Temperature,CPU_Power,IO_Power])
        print("Current Time: ",current_time)
        print("SoC_Temperature: ",SoC_Temperature)
        print("CPU_Power: ",CPU_Power)
        print("IO_Power: ",IO_Power)
        header_flag = False 
        time.sleep(2)  # Wait for two seconds before running the command again
        print("------------------------------------------------------------------------------------")
        print()
