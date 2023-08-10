frequencies=[('999', '', 'MHz'), ('1000', '', 'MHz'), ('876', '', 'MHz'), ('1000', '', 'MHz'), ('1.07', '.07', 'GHz'), ('546', '', 'MHz'), ('2.80', '.80', 'GHz'), ('1000', '', 'MHz'), ('1000', '', 'MHz'), ('1.02', '.02', 'GHz'), ('1.04', '.04', 'GHz'), ('1000', '', 'MHz'), ('1.09', '.09', 'GHz'), ('1.05', '.05', 'GHz'), ('1.09', '.09', 'GHz'), ('1.32', '.32', 'GHz'), ('1.04', '.04', 'GHz'), ('2.80', '.80', 'GHz'), ('765', '', 'MHz'),  ('1000', '', 'MHz')]
formatted_frequencies=[]
for freq in frequencies:
    value, unit = float(freq[0]), freq[2]
    if unit == 'MHz':
        value /= 1000  # Convert MHz to GHz
    formatted_frequencies.append(float(f"{value:.2f}"))

print(formatted_frequencies)
