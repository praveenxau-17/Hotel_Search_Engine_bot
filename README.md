# Global Hotel Search Telegram Bot

A complete Telegram chatbot that functions as a hotel search engine across the world. Built with Python and `python-telegram-bot`, using local mock data.

## 🚀 Features

- **Global Search**: Find hotels in 10+ major cities (Paris, New York, London, Tokyo, etc.).
- **Rich UI**: Interactive inline keyboards, emojis, and formatted Markdown messages.
- **Sorting**: Sort results by price or rating.
- **Mock Booking**: Complete multi-step booking flow with date validation.
- **Session Management**: Supports multiple users simultaneously.
- **Mock Data**: Pre-loaded with 15+ hotels (Budget, Mid-range, Luxury).

## 📂 Structure

- `backend/`: Core logic and data.
  - `data/`: JSON mock database.
  - `models/`: Hotel and Booking data structures.
  - `services/`: Search, Booking, and Session logic.
  - `utils/`: Validators and formatters.
- `frontend/`: Telegram bot interface.
  - `handlers/`: Command and conversation logic.
  - `keyboards/`: Inline keyboard builders.
  - `messages/`: Markdown templates.
- `main.py`: Root entry point to start the bot.

## 🛠️ Setup Instructions

1. **Clone the repository** (or ensure you have the files in your directory).
2. **Install dependencies**:
   If `pip` is not recognized, use `python -m pip`:
   ```bash
   python -m pip install -r backend/requirements.txt
   ```
3. **Configure the Bot Token**:
   - Open `backend/.env`.
   - Replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` with your actual token from [@BotFather](https://t.me/botfather).
4. **Mock API Configuration**:
   - The bot is configured to fetch data from your provided Mock API: `https://69e73bbe68208c1debe8820a.mockapi.io/api/hotels`.
   - If the API is unavailable, it gracefully falls back to the `backend/data/hotel_data.json` file.
5. **Run the bot**:
   ```bash
   python main.py
   ```

## 🤖 Commands

- `/start` - Welcome message and features.
- `/search` - Start searching for hotels by city.
- `/cities` - List all supported cities.
- `/help` - Show all available commands.
- `/cancel` - Cancel the current search or booking flow.

## 📅 Booking Flow

1. Type `/search` and enter a city (e.g., "Paris").
2. Select a hotel from the results.
3. Click "Book Now".
4. Enter dates in `YYYY-MM-DD to YYYY-MM-DD` format.
5. Review the summary and type `CONFIRM` to finalize.
6. Receive your unique mock Booking ID!

---
*Note: This is a demonstration bot using mock data. No real payments or bookings are made.*
