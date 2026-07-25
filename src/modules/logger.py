import logging

logging.basicConfig(
    filename="logs/detection.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_detection(message):
    logging.info(message)