import requests

# Importing the FLAMES game
from .flames import flames

# Importing the XO (Tic-Tac-Toe) game
from .xo import xo

# Importing the Chess game
from .chess_game import chess

def get_version_from_pypi():
    """Fetch the latest version of the rupi library from PyPI."""
    try:
        response = requests.get("https://pypi.org/pypi/rupi/json", timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return data["info"]["version"]
    except Exception:
        return "Unknown (Could not fetch from PyPI)"

def about():
    """Generate an about message with library details."""
    version = get_version_from_pypi()
    about_message = f"""
    Rupi Library:
    This library implements:
    1. FLAMES game: A fun relationship game based on two names.
    2. XO (Tic-Tac-Toe) game: A GUI-based game for two players built with Tkinter.
    3. Chess game: A GUI-based interactive chess game.

    PyPI: https://pypi.org/project/rupi/
    Author: Tanujairam
    Email: tanujairam.v@gmail.com
    Version: {version}
    """
    return about_message

def available_games():
    """Print the list of games available in the rupi library."""
    games = ["FLAMES", "Tic-Tac-Toe", "Chess"]
    print("Available games in rupi:")
    for game in games:
        print(f"- {game}")

# Exported functions for games
__all__ = ["flames", "xo", "chess", "get_about_message", "available_games"]
