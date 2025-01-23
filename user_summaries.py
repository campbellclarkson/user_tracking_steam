import requests
import pandas as pd
import time
import os

API_KEY = "00E64D0529645F775F3261124FAAB908"

# Input and output file paths
input_csv = "./data/steamid_sample.csv"
output_csv = "./data/steam_player_data.csv"

# Steam API endpoints
PLAYER_SUMMARY_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

# Load sampled SteamIDs
df = pd.read_csv(input_csv)
all_steamids = df["steamid"].astype(str).tolist()

# Check for existing progress
if os.path.exists(output_csv):
    processed_df = pd.read_csv(output_csv)
    processed_steamids = processed_df["steamid"].astype(str).tolist()
else:
    processed_steamids = []

# Filter unprocessed steamIDs
remaining_steamids = [sid for sid in all_steamids if sid not in processed_steamids]

print(f"Resuming from {len(processed_steamids)} processed users. {len(remaining_steamids)} users remaining.")

def get_player_summary(steamid, retries=3):
    """Fetch player summary from the Steam API."""
    for attempt in range(retries):
        try:
            params = {"key": API_KEY, "steamids": steamid}
            response = requests.get(PLAYER_SUMMARY_URL, params=params, timeout=10)
            response.raise_for_status()  # Raise HTTP errors if any
            data = response.json()
            if "players" in data["response"] and data["response"]["players"]:
                return data["response"]["players"][0]  # Return the first player's info
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching player summary for {steamid}: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(2)  # Wait before retrying
    return None  # Return None if all attempts fail

def get_recent_playtime(steamid, retries=3):
    """Fetch recent playtime (last two weeks) from the Steam API."""
    for attempt in range(retries):
        try:
            params = {"key": API_KEY, "steamid": steamid, "include_played_free_games": True}
            response = requests.get(OWNED_GAMES_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if "games" in data["response"]:
                total_playtime = sum(game.get("playtime_2weeks", 0) for game in data["response"]["games"])
                return total_playtime / 60  # Convert minutes to hours
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching recent playtime for {steamid}: {e}. Attempt {attempt + 1} of {retries}")
            time.sleep(2)  # Wait before retrying
    return 0.0  # Return 0.0 if all attempts fail

# Process remaining SteamIDs
for idx, steamid in enumerate(remaining_steamids, start=1):
    print(f"Processing SteamID {idx}/{len(remaining_steamids)}: {steamid}")

    summary = get_player_summary(steamid)
    recent_playtime = get_recent_playtime(steamid)

    if summary:
        entry = {
            "steamid": steamid,
            "personaname": summary.get("personaname", ""),
            "loccountrycode": summary.get("loccountrycode", ""),
            "recent_playtime_hours": round(recent_playtime, 2),
            "profileurl": summary.get("profileurl", "")
        }

        # Save incrementally
        pd.DataFrame([entry]).to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False, encoding="utf-8")

    # Save progress every 500 users
    if idx % 500 == 0:
        print(f"Checkpoint saved at {idx} new entries.")

    time.sleep(0.5)

print(f"Player data saved to {output_csv}")
