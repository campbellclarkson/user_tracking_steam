import steamreviews

with open("id_list.txt", "r") as file:
    app_ids = [int(line.strip()) for line in file if line.strip().isdigit()]

request_params = dict()
request_params['day_range'] = '28'

steamreviews.download_reviews_for_app_id_batch(app_ids, chosen_request_params=request_params)