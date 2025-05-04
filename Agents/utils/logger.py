import logging
import os
from datetime import datetime

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file with timestamp
log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
log_path = os.path.join(LOG_DIR, log_filename)

# Logger setup
logger = logging.getLogger("LangGraphApp")
logger.setLevel(logging.DEBUG)  # Set to INFO or ERROR for less verbosity

# File Handler
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)

# Console Handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
