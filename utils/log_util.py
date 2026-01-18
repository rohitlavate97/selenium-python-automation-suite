import logging
import json
import os
import uuid
from threading import local
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler

_thread_ctx = local()


class MaskingFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        for secret in ["password", "pwd", "secret", "token"]:
            msg = msg.replace(secret, "****")
        record.msg = msg
        return True


class LogUtil:

    @staticmethod
    def set_context(test_name, env, browser):
        correlation_id = str(uuid.uuid4())[:8]
        _thread_ctx.correlation_id = correlation_id
        _thread_ctx.test_name = test_name
        _thread_ctx.env = env
        _thread_ctx.browser = browser

        _thread_ctx.log_file = f"logs/test_{correlation_id}.log"
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

            combined = RotatingFileHandler(
                "logs/automation.log", maxBytes=5_000_000, backupCount=5
            )
            combined.setFormatter(formatter)
            combined.addFilter(MaskingFilter())

            per_test_file = getattr(_thread_ctx, "log_file", "logs/default.log")
            per_test = logging.FileHandler(per_test_file)
            per_test.setFormatter(formatter)
            per_test.addFilter(MaskingFilter())

            console = logging.StreamHandler()
            console.setFormatter(formatter)

            logger.addHandler(combined)
            logger.addHandler(per_test)
            logger.addHandler(console)

        return logger

    @staticmethod
    def log_json(message, level="INFO", extra=None):
        os.makedirs("logs", exist_ok=True)

        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "message": message,
            **LogUtil.get_context()
        }

        if extra:
            payload.update(extra)

        with open("logs/structured.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
