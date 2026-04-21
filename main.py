import sys
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add the project root to sys.path to allow imports from backend and frontend
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from frontend.bot import create_application

# Simple server to satisfy Render's port check for Web Services
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
    
    def log_message(self, format, *args):
        # Silence standard HTTP logging to keep Render logs clean
        return

def run_health_server():
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    print(f"✅ Health check server started on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    # Start the health check server in a background thread
    threading.Thread(target=run_health_server, daemon=True).start()

    app = create_application()
    if app:
        print("🌍 Global Hotel Search Bot is online!")
        print("Press Ctrl+C to stop.")
        app.run_polling()
    else:
        print("❌ Failed to start bot. Check your BOT_TOKEN in backend/.env")
