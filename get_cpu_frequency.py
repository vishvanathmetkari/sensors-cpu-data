import subprocess
import re
import time
import csv
import json
from datetime import datetime

command1 = "cpupower -c 0-95 frequency-info"
csv_file1 = "cpu_frequency_data.csv"

def get_cpu_freq(text):
    cpu_pattern = re.compile(r"analyzing CPU (\d+):")
    frequency_pattern = re.compile(r'current CPU frequency:\s+(\d+(\.\d*)?)\s+(GHz|MHz)')
    cpu_matches = cpu_pattern.findall(text)
    frequency_matches = frequency_pattern.findall(text)
    return cpu_matches, frequency_matches

with open(csv_file1, mode="a", newline="") as file1:
    writer1 = csv.writer(file1)
    first_iteration = True
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
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()
        print("len_cpu_matches:", len(cpu_matches))
        print("len_cpu_freq:", len(formatted_frequencies))
        print()
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

        if first_iteration:
            writer1.writerow([f"CPU {i}" for i in cpu_matches])
            first_iteration = False

        writer1.writerow(formatted_frequencies)
        time.sleep(2)
        print()
