import functools
import allure
from utils.log_util import LogUtil


def log_step(step_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = LogUtil.get_logger(func.__module__)
            logger.info(f"STEP START: {step_name}")
            LogUtil.log_json("Step started", extra={"step": step_name})

            with allure.step(step_name):
                try:
                    result = func(*args, **kwargs)
                    logger.info(f"STEP PASS: {step_name}")
                    LogUtil.log_json("Step passed", extra={"step": step_name})
                    return result
                except Exception as e:
                    logger.error(f"STEP FAIL: {step_name} | {e}")
                    LogUtil.log_json(
                        "Step failed",
                        level="ERROR",
                        extra={"step": step_name, "error": str(e)}
                    )
                    raise
        return wrapper
    return decorator
