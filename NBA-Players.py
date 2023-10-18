import requests  # Import the 'requests' library to make HTTP requests.
import csv       # Import the 'csv' module to work with CSV files.

# Define the URL for the NBA player data API from RapidAPI.
url = "https://free-nba.p.rapidapi.com/players"

# Define the initial parameters for pagination.
per_page = 100  # Number of results to retrieve per page.
page = 1        # Initialize the page number.
all_player_data = []  # Create an empty list to store all player data.

# Set the headers required for the RapidAPI request.
headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",        # Replace with your actual API key.
    "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
}

# Start an infinite loop to retrieve data from multiple pages.
while True:
    # Set the parameters for the current page.
    querystring = {"page": str(page), "per_page": str(per_page)}

    # Send a GET request to the API with the specified URL, headers, and query parameters.
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:  # Check if the request was successful (HTTP status code 200).
        data = response.json()  # Parse the JSON response into a Python dictionary.

        # Extract player data from the 'data' list and append it to the 'all_player_data' list.
        for player in data['data']:
            player_id = player['id']
            first_name = player['first_name']
            last_name = player['last_name']
            position = player['position']
            team_name = player['team']['full_name']

            all_player_data.append([player_id, first_name, last_name, position, team_name])

        # Check if there are more pages to retrieve based on total_count.
        if page * per_page >= data['meta']['total_count']:
            break  # Exit the loop if all data has been retrieved.

        # Increment the page number for the next request.
        page += 1
    else:
        # Print an error message and exit the loop if the request fails.
        print(f"Failed to get data for page {page}. Status code: {response.status_code}")
        break

# Define the CSV file name and headers.
csv_filename = "nba_players_all.csv"
csv_headers = ["Player ID", "First Name", "Last Name", "Position", "Team Name"]

# Create a CSV file and write the data.
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)  # Write the header row.
    csv_writer.writerows(all_player_data)  # Write all player data rows.

print(f"Data has been successfully written to {csv_filename}")

