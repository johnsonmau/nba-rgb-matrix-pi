import time
import requests
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
from io import BytesIO

# Configuration for the LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust as per your setup
matrix = RGBMatrix(options=options)

# Fonts and colors
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
white = graphics.Color(255, 255, 255)
red = graphics.Color(255, 0, 0)
green = graphics.Color(0, 255, 0)

# API endpoints and keys
odds_api_url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
odds_api_key = "YOUR_ODDS_API_KEY"
nba_api_url = "https://www.balldontlie.io/api/v1/games"
team_logos = {
    "Lakers": "path/to/lakers_logo.png",
    "Warriors": "path/to/warriors_logo.png",
    # Add paths to all team logos
}

def fetch_game_data():
    # Fetch today's NBA games
    response = requests.get(nba_api_url, params={"start_date": "2025-02-21", "end_date": "2025-02-21"})
    games = response.json()["data"]
    return games

def fetch_betting_odds():
    # Fetch betting odds
    response = requests.get(odds_api_url, params={"apiKey": odds_api_key, "regions": "us"})
    odds = response.json()
    return odds

def display_game_info(game, odds):
    # Clear the matrix
    matrix.Clear()

    # Display team logos
    home_team = game["home_team"]["full_name"]
    visitor_team = game["visitor_team"]["full_name"]
    home_logo = Image.open(team_logos[home_team])
    visitor_logo = Image.open(team_logos[visitor_team])
    matrix.SetImage(home_logo.convert('RGB'), 0, 0)
    matrix.SetImage(visitor_logo.convert('RGB'), 32, 0)

    # Display game time or live score
    if game["status"] == "scheduled":
        start_time = game["start_time"]  # Adjust time format as needed
        graphics.DrawText(matrix, font, 2, 30, white, f"{start_time}")
        # Display betting odds
        game_odds = next((o for o in odds if o["home_team"] == home_team and o["away_team"] == visitor_team), None)
        if game_odds:
            home_odds = game_odds["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
            away_odds = game_odds["bookmakers"][0]["markets"][0]["outcomes"][1]["price"]
            graphics.DrawText(matrix, font, 2, 40, green, f"{home_team}: {home_odds}")
            graphics.DrawText(matrix, font, 2, 50, red, f"{visitor_team}: {away_odds}")
    elif game["status"] == "in_progress":
        home_score = game["home_team_score"]
        visitor_score = game["visitor_team_score"]
        period = game["period"]
        time_remaining = game["time"]
        graphics.DrawText(matrix, font, 2, 30, white, f"{home_score} - {visitor_score}")
        graphics.DrawText(matrix, font, 2, 40, white, f"Q{period} {time_remaining}")

    # Hold the display for a few seconds
    time.sleep(5)

def main():
    games = fetch_game_data()
    odds = fetch_betting_odds()
    for game in games:
        display_game_info(game, odds)

if __name__ == "__main__":
    main()
