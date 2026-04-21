import sys
import os

# Add the project root to sys.path to allow imports from backend and frontend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.bot import create_application

if __name__ == "__main__":
    app = create_application()
    if app:
        print("🌍 Global Hotel Search Bot is online!")
        print("Press Ctrl+C to stop.")
        app.run_polling()
    else:
        print("❌ Failed to start bot. Check your BOT_TOKEN in backend/.env")
