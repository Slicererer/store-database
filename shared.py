import os
import json
from datetime import datetime
import platform
import random

CUSTOM_MOODS_FILE = "custom_moods.json"
MOOD_LOG_FILE = "mood_log.txt"
TASKS_FILE = "tasks.json"
QUOTES_FILE = "quotes.json"

DEFAULT_MOODS = {
    "😊": "Happy",
    "😢": "Sad",
    "😡": "Angry",
    "😌": "Relaxed",
    "😴": "Tired",
    "😐": "Neutral",
}

MOOD_TASKS_SUGGESTIONS = {
    "😊": [
        "Celebrate your happiness!",
        "Share your joy with a friend",
        "Do something creative",
        "Write a gratitude list",
        "Take a joyful walk outside",
        "Listen to your favorite upbeat music",
        "Plan a fun activity for the weekend"
    ],
    "😢": [
        "Take some rest",
        "Talk to a friend",
        "Write down your feelings",
        "Watch a comforting movie",
        "Try gentle stretching or yoga",
        "Meditate for a few minutes",
        "Treat yourself kindly today"
    ],
    "😡": [
        "Try some deep breathing",
        "Go for a walk",
        "Listen to calming music",
        "Write down what’s bothering you",
        "Take a timeout to cool down",
        "Do some physical exercise",
        "Try a creative outlet like drawing"
    ],
    "😌": [
        "Meditate for 10 minutes",
        "Read a book",
        "Take a relaxing bath",
        "Practice mindful breathing",
        "Write in a journal",
        "Spend time in nature",
        "Do some light stretching"
    ],
    "😴": [
        "Go to bed early",
        "Avoid screens before sleep",
        "Try gentle stretches",
        "Drink a cup of herbal tea",
        "Create a calm sleep environment",
        "Read a relaxing book",
        "Practice deep breathing"
    ],
    "😐": [
        "Plan your day",
        "Organize your workspace",
        "Take short breaks",
        "Do a quick tidy up",
        "Review your goals",
        "Try a new hobby",
        "Reach out to a friend"
    ],
}

# Expanded quotes list:
DEFAULT_QUOTES = [
    "Believe you can and you're halfway there.",
    "Keep going, you are getting there.",
    "Every day is a new beginning.",
    "You are stronger than you think.",
    "Progress, not perfection.",
    "Happiness is a journey, not a destination.",
    "Small steps every day lead to big results.",
    "Take a deep breath and start again.",
    "Your feelings are valid.",
    "Keep your face to the sunshine and you cannot see a shadow.",
    "The best way out is always through.",
    "Turn your wounds into wisdom.",
    "Do what you can, with what you have, where you are.",
    "Stay positive, work hard, make it happen.",
    "Rest and self-care are so important."
]

def beep():
    if platform.system() == "Windows":
        try:
            import winsound
            winsound.Beep(1000, 150)
        except Exception:
            pass
    else:
        print("\a", end="")

def load_json(filename, default=None):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default if default is not None else {}
    return default if default is not None else {}

def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def load_custom_moods():
    return load_json(CUSTOM_MOODS_FILE, {})

def save_custom_moods(custom_moods):
    save_json(CUSTOM_MOODS_FILE, custom_moods)

def log_mood(mood_emoji, mood_name):
    try:
        with open(MOOD_LOG_FILE, "a", encoding="utf-8") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{now} - {mood_emoji} {mood_name}\n")
        beep()
    except Exception as e:
        print(f"Error logging mood: {e}")

def count_logged_days():
    if not os.path.exists(MOOD_LOG_FILE):
        return 0
    try:
        with open(MOOD_LOG_FILE, "r", encoding="utf-8") as f:
            dates = set()
            for line in f:
                if line.strip():
                    date_part = line.split(" ")[0]
                    dates.add(date_part)
            return len(dates)
    except Exception:
        return 0

def load_tasks():
    return load_json(TASKS_FILE, [])

def save_tasks(tasks):
    save_json(TASKS_FILE, tasks)

def get_daily_quote():
    quotes = load_json(QUOTES_FILE, DEFAULT_QUOTES)
    return random.choice(quotes)
