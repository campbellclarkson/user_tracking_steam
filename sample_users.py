import pandas as pd

input_csv = "./data/combined_reviews.csv"
output_csv = "./data/steamid_sample.csv"

df = pd.read_csv(input_csv, usecols=["steamid", "num_games_owned", "language"])

df_filtered = df[df["num_games_owned"] > 0]

df_english = df_filtered[df_filtered["language"] == "english"]

unique_steamids = df_english["steamid"].drop_duplicates()

sample_size = 40000
sampled_steamids = unique_steamids.sample(n=sample_size, random_state=123)

sampled_steamids.to_csv(output_csv, index=False, header=["steamid"])

print(f"Sampled {sample_size} unique SteamIDs saved to {output_csv}")