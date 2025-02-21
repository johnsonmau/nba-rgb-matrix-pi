import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

# LED Matrix Configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust as needed
matrix = RGBMatrix(options=options)

# Fonts and Colors
font = graphics.Font()
font.LoadFont("rpi-rgb-led-matrix/fonts/7x13.bdf")
white = graphics.Color(255, 255, 255)
red = graphics.Color(255, 0, 0)
green = graphics.Color(0, 255, 0)

# Team Logos (Adjust paths based on your setup)
TEAM_LOGOS = {
    "BOS": "assets/boston.png",
    "ATL": "assets/atlanta.png",
    "LAL": "assets/lakers.png",
    "MIA": "assets/heat.png",
    # Add more team logos...
}

# Static Game Data (Simulated API Response)
GAMES = [
    {
        "home_team": {"full_name": "Boston Celtics", "abbreviation": "BOS"},
        "visitor_team": {"full_name": "Atlanta Hawks", "abbreviation": "ATL"},
        "status": "scheduled",
        "start_time": "7:30 PM ET",
        "odds": {"home": "-250", "away": "+200"}
    },
    {
        "home_team": {"full_name": "Los Angeles Lakers", "abbreviation": "LAL"},
        "visitor_team": {"full_name": "Miami Heat", "abbreviation": "MIA"},
        "status": "in_progress",
        "home_team_score": 78,
        "visitor_team_score": 65,
        "period": 3,
        "time_remaining": "8:42"
    }
]

def get_team_logo(team_abbr):
    """Returns the path to a team's logo."""
    return TEAM_LOGOS.get(team_abbr, "assets/default.png")  # Use default image if not found

def display_game_info(game):
    """Displays game details on the LED matrix."""
    matrix.Clear()

    home_abbr = game["home_team"]["abbreviation"]
    visitor_abbr = game["visitor_team"]["abbreviation"]

    # Load and display team logos
    try:
        home_logo = Image.open(get_team_logo(home_abbr)).convert("RGB")
        visitor_logo = Image.open(get_team_logo(visitor_abbr)).convert("RGB")
        matrix.SetImage(home_logo, 0, 0)
        matrix.SetImage(visitor_logo, 32, 0)
    except Exception as e:
        print(f"Error loading team logos: {e}")

    # Display game time or live score
    if game["status"] == "scheduled":
        start_time = game["start_time"]
        graphics.DrawText(matrix, font, 2, 30, white, f"Start: {start_time}")

        # Display betting odds
        home_odds = game["odds"]["home"]
        away_odds = game["odds"]["away"]
        graphics.DrawText(matrix, font, 2, 40, green, f"{home_abbr}: {home_odds}")
        graphics.DrawText(matrix, font, 2, 50, red, f"{visitor_abbr}: {away_odds}")

    elif game["status"] == "in_progress":
        home_score = game["home_team_score"]
        visitor_score = game["visitor_team_score"]
        period = game["period"]
        time_remaining = game["time_remaining"]
        graphics.DrawText(matrix, font, 2, 30, white, f"{home_score} - {visitor_score}")
        graphics.DrawText(matrix, font, 2, 40, white, f"Q{period} {time_remaining}")

    time.sleep(5)  # Display each game for 5 seconds

def main():
    """Main loop that cycles through static game data."""
    while True:
        for game in GAMES:
            display_game_info(game)

if __name__ == "__main__":
    main()
