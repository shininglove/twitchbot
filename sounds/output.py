import logging, os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("download_logger")

logger.setLevel(logging.DEBUG)

filename = "download.log"

# Use Path module.
bot_log = os.path.join(os.getcwd(), "logs", filename)

filelog = RotatingFileHandler(bot_log, maxBytes=20000, backupCount=5)

filelog.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "[ %(asctime)s ] : %(levelname)s in %(filename)s : %(message)s"
)

filelog.setFormatter(formatter)

logger.addHandler(filelog)
