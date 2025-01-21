import pandas as pd

input_csv = "./data/steamid_sample.csv" 

df = pd.read_csv(input_csv)

duplicates = df[df.duplicated()]

if not duplicates.empty:
    print("Duplicate rows found:")
    print(duplicates)
else:
    print("No duplicate rows found.")
