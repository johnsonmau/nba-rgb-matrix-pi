import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont

# Configuration for the LED matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular'  # Adjust as per your setup
matrix = RGBMatrix(options=options)

# Create a blank image
image = Image.new("RGB", (options.cols, options.rows))
draw = ImageDraw.Draw(image)

# Load font
font = ImageFont.load_default()

# Team logos
team_logos = {
    "BOS": "assets/boston.png",
    "ATL": "assets/atlanta.png"
}

# Static game data (mocked instead of API calls)
games = [
    {
        "home_team": "BOS",
        "visitor_team": "ATL",
        "status": "in_progress",
        "home_score": 53,
        "visitor_score": 28,
        "period": 2,
        "time": "4:02"
    },
    {
        "home_team": "MIA",
        "visitor_team": "NYK",
        "status": "scheduled",
        "start_time": "7:30 PM"
    }
]

def load_team_logo(team_code):
    """Load and resize team logo if available."""
    if team_code in team_logos:
        img = Image.open(team_logos[team_code])
        return img.resize((30, 30))  # Resize to fit matrix
    return None

def display_game_info(game):
    """Render and display game information on LED matrix."""
    draw.rectangle((0, 0, options.cols, options.rows), fill=(0, 0, 0))  # Clear screen

    # Load team logos
    home_logo = load_team_logo(game["home_team"])
    visitor_logo = load_team_logo(game["visitor_team"])

    if home_logo:
        image.paste(home_logo, (0, 1))  # Place home team logo
    if visitor_logo:
        image.paste(visitor_logo, (32, 1))  # Place away team logo

    # Display game status
    if game["status"] == "scheduled":
        draw.text((2, 20), f"{game['home_team']} vs {game['visitor_team']}", font=font, fill=(255, 255, 255))
        draw.text((2, 25), f"Start: {game['start_time']}", font=font, fill=(255, 255, 255))
    elif game["status"] == "in_progress":
        draw.text((2, 20), f"{game['home_team']} {game['home_score']} - {game['visitor_score']} {game['visitor_team']}",
                  font=font, fill=(255, 255, 255))
        draw.text((2, 25), f"Q{game['period']} | {game['time']}", font=font, fill=(255, 255, 255))

    # Display the image on the matrix
    matrix.SetImage(image)

    # Hold for 5 seconds before next update
    time.sleep(5)

def main():
    """Main loop to display games on the matrix."""
    while True:
        for game in games:
            display_game_info(game)

if __name__ == "__main__":
    main()
