"""
Configuration settings for AppFolio automation system
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "appfolio"
LOGS_DIR = BASE_DIR / "logs"

# AppFolio settings
APPFOLIO_CONFIG = {
    "username": os.getenv("APPFOLIO_EMAIL"),  # Using email as username
    "password": os.getenv("APPFOLIO_PASSWORD"),
    "base_url": os.getenv("APPFOLIO_URL"),
    "login_timeout": 30,
    "download_timeout": 60,
}

# Browser settings
BROWSER_CONFIG = {
    "headless": False,  # Using visible browser for better control
    "use_existing_browser": True,  # Connect to existing Chrome instance
    "browser_type": "chromium",  # Use chromium (Chrome-compatible)
    "viewport": {"width": 1920, "height": 1080},
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "downloads_path": str(DATA_DIR),
    "chrome_executable_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # macOS Chrome path
    "remote_debugging_port": 9222,  # Port for connecting to existing Chrome
    "connect_to_existing": True,  # Flag to connect rather than launch new
    "profile_directory": "Profile 1",  # Chrome profile directory (Profile 1 = Person 1)
    "user_data_dir": os.path.expanduser("~/Library/Application Support/Google/Chrome"),  # Chrome user data directory on macOS
}

# File paths
PATHS = {
    "ledgers": DATA_DIR / "ledgers",
    "analyzed": DATA_DIR / "analyzed", 
    "leases": DATA_DIR / "leases",
    "pmas": DATA_DIR / "pmas",
    "work_orders": DATA_DIR / "work-orders",
    "logs": LOGS_DIR,
}

# Google Drive settings
GOOGLE_DRIVE_CONFIG = {
    "folder_id": os.getenv("GOOGLE_DRIVE_FOLDER_ID"),
    "credentials_file": BASE_DIR / "config" / "google_credentials.json",
    "token_file": BASE_DIR / "config" / "google_token.json",
}

# SMS settings
SMS_CONFIG = {
    "twilio_sid": os.getenv("TWILIO_ACCOUNT_SID"),
    "twilio_token": os.getenv("TWILIO_AUTH_TOKEN"),
    "from_number": os.getenv("TWILIO_PHONE_NUMBER"),
    "to_number": os.getenv("ALERT_PHONE_NUMBER"),
}

# AI settings
AI_CONFIG = {
    "gemini_api_key": os.getenv("GEMINI_API_KEY"),
    "openai_api_key": os.getenv("OPENAI_API_KEY"),
    "model": "gpt-4o-mini",  # Using OpenAI as primary model
}

# Automation schedule
SCHEDULE_CONFIG = {
    "daily_run_time": "09:00",  # 9 AM daily
    "retry_attempts": 3,
    "retry_delay": 300,  # 5 minutes
}

# Create directories if they don't exist
for path in PATHS.values():
    path.mkdir(parents=True, exist_ok=True)