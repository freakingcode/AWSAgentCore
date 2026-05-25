import logging
import os
import sys

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("InventoryAI")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

if not logger.handlers:

    # Console logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File logs
    file_handler = logging.FileHandler("logs/app.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

logger.propagate = False