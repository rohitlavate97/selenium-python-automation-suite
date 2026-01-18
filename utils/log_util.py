import logging
import json
import os
import uuid
from threading import local
from datetime import datetime

_thread_ctx = local()


class LogUtil:

    @staticmethod
    def set_context(test_name, env, browser):
        correlation_id = str(uuid.uuid4())[:8]
        _thread_ctx.correlation_id = correlation_id
        _thread_ctx.test_name = test_name
        _thread_ctx.env = env
        _thread_ctx.browser = browser
        return correlation_id

    @staticmethod
    def get_context():
        return {
            "correlation_id": getattr(_thread_ctx, "correlation_id", "N/A"),
            "test_name": getattr(_thread_ctx, "test_name", "N/A"),
            "env": getattr(_thread_ctx, "env", "N/A"),
            "browser": getattr(_thread_ctx, "browser", "N/A")
        }

    @staticmethod
    def get_logger(name):
        os.makedirs("logs", exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
            )

            fh = logging.FileHandler("logs/automation.log")
            fh.setFormatter(formatter)

            ch = logging.StreamHandler()
            ch.setFormatter(formatter)

            logger.addHandler(fh)
            logger.addHandler(ch)

        return logger

    @staticmethod
    def log_json(message, level="INFO", extra=None):
        os.makedirs("logs", exist_ok=True)

        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            **LogUtil.get_context()
        }

        if extra:
            payload.update(extra)

        with open("logs/structured.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
