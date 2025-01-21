import requests
import pandas as pd
import time

API_KEY = "00E64D0529645F775F3261124FAAB908"

# Input and output file paths
input_csv = "./data/steamid_sample.csv"
output_csv = "./data/steam_player_data.csv"

# Steam API endpoints
PLAYER_SUMMARY_URL = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
OWNED_GAMES_URL = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"

# Load sampled SteamIDs
df = pd.read_csv(input_csv)
df = df.head(10)
steamids = df["steamid"].astype(str).tolist()

# List to store results
player_data = []

def get_player_summary(steamid):
    """Fetch player summary from the Steam API."""
    params = {
        "key": API_KEY,
        "steamids": steamid
    }
    response = requests.get(PLAYER_SUMMARY_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "players" in data["response"] and data["response"]["players"]:
            return data["response"]["players"][0]  # Return the first player's info
    return None

def get_recent_playtime(steamid):
    """Fetch recent playtime (last two weeks) from the Steam API."""
    params = {
        "key": API_KEY,
        "steamid": steamid,
        "include_played_free_games": True
    }
    response = requests.get(OWNED_GAMES_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "games" in data["response"]:
            total_playtime = sum(game.get("playtime_2weeks", 0) for game in data["response"]["games"])
            return total_playtime / 60  # Convert minutes to hours
    return 0.0

# Loop through the SteamIDs and fetch data
for steamid in steamids:
    print(f"Processing SteamID: {steamid}")
    
    summary = get_player_summary(steamid)
    recent_playtime = get_recent_playtime(steamid)

    if summary:
        player_data.append({
            "steamid": steamid,
            "personaname": summary.get("personaname", ""),
            "loccountrycode": summary.get("loccountrycode", ""),
            "recent_playtime_hours": round(recent_playtime, 2),
            "profileurl": summary.get("profileurl", "")
        })

    # To avoid hitting API rate limits, add a delay
    time.sleep(1)

# Convert the list to a DataFrame and save it to CSV
output_df = pd.DataFrame(player_data)
output_df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"Player data saved to {output_csv}")