import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Configure logging
directory = os.getcwd() + "/storage"
if not os.path.exists(directory):
    os.makedirs(directory)


log_file_path = os.path.join(directory, "app.log")

handler = TimedRotatingFileHandler(
    filename=log_file_path,
    when="midnight",  # Rotate the log at midnight
    interval=1,  # The interval at which the log file is rotated (1 day)
    backupCount=7,  # Keep 7 days' worth of logs; older logs will be deleted
    encoding="utf-8"
)

# Set up the logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
