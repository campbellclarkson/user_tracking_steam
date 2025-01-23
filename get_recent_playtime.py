import requests
import pandas as pd
import time
import os

API_KEY = "00E64D0529645F775F3261124FAAB908"

# Input and output file paths
input_csv = "./data/steam_player_data.csv"
output_csv = "./data/steam_player_data_updated.csv"

# Steam API endpoint for recently played games
RECENTLY_PLAYED_URL = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/"

# Load SteamIDs from the existing CSV
df = pd.read_csv(input_csv)

# Check if progress file exists and resume from where it left off
if os.path.exists(output_csv):
    df_saved = pd.read_csv(output_csv)
    processed_steamids = set(df_saved["steamid"].astype(str))
    df["two_weeks"] = df_saved["two_weeks"]  # Carry over existing progress
else:
    processed_steamids = set()
    df["two_weeks"] = None  # Initialize the column if not present

# Function to get playtime for the last two weeks
def get_recent_playtime(steamid, retries=3):
    for attempt in range(retries):
        try:
            params = {"key": API_KEY, "steamid": steamid}
            response = requests.get(RECENTLY_PLAYED_URL, params=params, timeout=10)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            if "games" in data["response"]:
                total_playtime = sum(game.get("playtime_2weeks", 0) for game in data["response"]["games"])
                return round(total_playtime / 60, 2)  # Convert minutes to hours
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching recent playtime for {steamid}: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(2)  # Wait before retrying
    return 0.0  # Return 0.0 if all attempts fail

# Fetch and update playtime data, resuming from the last processed SteamID
for index, row in df.iterrows():
    steamid = str(row["steamid"])
    
    if steamid in processed_steamids:
        continue  # Skip already processed SteamIDs

    df.at[index, "two_weeks"] = get_recent_playtime(steamid)
    print(f"Processed {index + 1}/{len(df)}: SteamID {steamid}")

    # Save progress after each iteration
    df.to_csv(output_csv, index=False, encoding="utf-8")
    time.sleep(1)  # Pause for 1 second to avoid hitting rate limits

print(f"Updated player data saved to {output_csv}")