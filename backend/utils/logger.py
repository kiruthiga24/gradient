import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # DEBUG/INFO/WARNING/ERROR/CRITICAL
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # prints to console during dev
    ]
)

# logger instance to use everywhere
logger = logging.getLogger("agentic_app")
