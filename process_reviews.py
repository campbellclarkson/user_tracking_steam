import os
import json
import pandas as pd

folder_path = "./data/"

all_reviews = []


for filename in os.listdir(folder_path):
    if filename.startswith("review_") and filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            # Extract reviews dictionary
            reviews = data.get("reviews", {})
            
            for review_id, review_data in reviews.items():
                author = review_data.get("author", {})
                
                # Flatten the review data into a single dictionary
                review_entry = {
                    "recommendationid": review_data.get("recommendationid"),
                    "steamid": author.get("steamid"),
                    "num_games_owned": author.get("num_games_owned"),
                    "num_reviews": author.get("num_reviews"),
                    "playtime_forever": author.get("playtime_forever"),
                    "playtime_last_two_weeks": author.get("playtime_last_two_weeks"),
                    "playtime_at_review": author.get("playtime_at_review"),
                    "last_played": author.get("last_played"),
                    "language": review_data.get("language"),
                    "timestamp_created": review_data.get("timestamp_created"),
                    "timestamp_updated": review_data.get("timestamp_updated"),
                    "voted_up": review_data.get("voted_up"),
                    "votes_up": review_data.get("votes_up"),
                    "votes_funny": review_data.get("votes_funny"),
                    "weighted_vote_score": review_data.get("weighted_vote_score"),
                    "comment_count": review_data.get("comment_count"),
                    "steam_purchase": review_data.get("steam_purchase"),
                    "received_for_free": review_data.get("received_for_free"),
                    "written_during_early_access": review_data.get("written_during_early_access"),
                    "primarily_steam_deck": review_data.get("primarily_steam_deck"),
                }
                
                all_reviews.append(review_entry)

df = pd.DataFrame(all_reviews)

output_csv = "./data/combined_reviews.csv"
df.to_csv(output_csv, index=False, encoding="utf-8")

print(f"CSV file saved as {output_csv}")
