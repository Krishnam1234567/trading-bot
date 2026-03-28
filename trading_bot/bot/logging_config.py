import logging
import sys
import json
from datetime import datetime

logger = logging.getLogger("trading_bot")

def setup_logging(log_file="bot.log", level=logging.INFO):
    logger.setLevel(level)

    logger.propagate = False

    if logger.handlers:
        return

    text_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s'
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(text_formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(text_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def log_api_call(method: str, endpoint: str, payload: dict = None, response: dict = None, status_code: int = None, error: str = None):
    log_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "method": method,
        "endpoint": endpoint,
        "status_code": status_code,
    }
    
    if payload:
        safe_payload = payload.copy()
        if "signature" in safe_payload:
            safe_payload["signature"] = "***"
        log_data["payload"] = safe_payload

    if response:
        log_data["response"] = response

    if error:
        log_data["error"] = error
        logger.error(f"API ERROR: {json.dumps(log_data)}")
    else:
        logger.info(f"API CALL: {json.dumps(log_data)}")

setup_logging()
