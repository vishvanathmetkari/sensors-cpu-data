import subprocess
import re
import time
import csv
import json
from datetime import datetime

command1 = "cpupower -c 0-95 frequency-info"
command2 = "sensors -j"
csv_file1 = "cpu_frequency_data.csv"
csv_file2 = "sensors_data.csv"

def get_cpu_freq(text):
    cpu_pattern = re.compile(r"analyzing CPU (\d+):")
    frequency_pattern = re.compile(r'current CPU frequency:\s+(\d+(\.\d*)?)\s+(GHz|MHz)')
    cpu_matches = cpu_pattern.findall(text)
    frequency_matches = frequency_pattern.findall(text)
    return cpu_matches, frequency_matches

with open(csv_file1, mode="a", newline="") as file1:
    writer1 = csv.writer(file1)
    first_iteration = True

    with open(csv_file2, "a", newline="") as file2:
        writer2 = csv.writer(file2)
        header_flag = True
        for _ in range(325):
            formatted_frequencies=[]
            cpu_frequency = subprocess.run(command1, shell=True, text=True, capture_output=True)
            cpu_matches, frequency_matches = get_cpu_freq(cpu_frequency.stdout)

            for freq in frequency_matches:
                value, unit = float(freq[0]), freq[2]
                if unit == 'MHz':
                    value /= 1000  # Convert MHz to GHz
                formatted_frequencies.append(float(f"{value:.2f}"))
            print()
            print("cpu_matches:", cpu_matches)
            print("frequency_matches:", formatted_frequencies)
            print()
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print()
            print("len_cpu_matches:", len(cpu_matches))
            print("len_cpu_freq:", len(formatted_frequencies))
            print()
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print()
            if first_iteration:
                writer1.writerow([f"CPU {i}" for i in cpu_matches])
                first_iteration = False

            writer1.writerow(formatted_frequencies)
            time.sleep(1)

            output = subprocess.run(command2, shell=True, text=True, capture_output=True)
            data=output.stdout
            parsed_data = json.loads(data)
            print(parsed_data["apm_xgene-isa-0000"])
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            SoC_Temperature=parsed_data["apm_xgene-isa-0000"]["SoC Temperature"]["temp1_input"]
            CPU_Power=parsed_data["apm_xgene-isa-0000"]["CPU power"]["power1_input"]
            IO_Power=parsed_data["apm_xgene-isa-0000"]["IO power"]["power2_input"]

            if header_flag:
                writer2.writerow(['Timestamp','SoC Temperature (°C)','CPU Power (W)','IO Power (W)'])
                header_flag = False
            writer2.writerow([current_time,SoC_Temperature,CPU_Power,IO_Power])
            print("Current Time: ",current_time)
            print("SoC_Temperature: ",SoC_Temperature)
            print("CPU_Power: ",CPU_Power)
            print("IO_Power: ",IO_Power)
            print()
            print('-----------------------------------------------------------------------------------------------------------------------')
            print()
            time.sleep(1)  # Wait for one seconds before running the command again
