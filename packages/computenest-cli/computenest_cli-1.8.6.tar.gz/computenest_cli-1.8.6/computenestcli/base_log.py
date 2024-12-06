import functools
import logging
import logging.config
import threading
import time
import traceback

import pkg_resources
import yaml
from computenestcli.exception.cli_common_exception import CliCommonException

from computenestcli.common.logging_constant import PROCESS_LOGGER, DEFAULT_PROGRESS, DEVELOPER_INFO_LOG_HANDLER_NAME, \
    LOGGING_CLOSURE_NAME
from computenestcli.common.logging_type import LoggingType

logging_initialized = False
global_config = None


class InfoWarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO or record.levelno == logging.WARNING


def load_process_config():
    global global_config
    if global_config is None:
        config_path = pkg_resources.resource_filename(__name__, PROCESS_LOGGER)  # 替换为实际文件
        with open(config_path, 'r') as file:
            global_config = yaml.safe_load(file)
    return global_config


def setup_logging(config_file='log.conf'):
    """Set up logging configuration from a configuration file."""
    global logging_initialized
    if not logging_initialized:
        # 获取配置文件的路径
        config_path = pkg_resources.resource_filename(__name__, config_file)
        logging.config.fileConfig(config_path)
        logging_initialized = True


def get_logger(name):
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def get_developer_logger():
    setup_logging()
    developer_logger = get_logger(LoggingType.DEVELOPER.value)
    for handler in developer_logger.handlers:
        if handler.get_name() == DEVELOPER_INFO_LOG_HANDLER_NAME:
            handler.addFilter(InfoWarningFilter())
    return developer_logger


def get_user_logger():
    setup_logging()
    return get_logger(LoggingType.USER.value)


def __get_inner_logger():
    setup_logging()
    return get_logger(LoggingType.INNER.value)


"""
Decorator to log the execution of a process.

:param service_name: Represents the execution of a CLI command, e.g., `import`.
:param process_name: A major step in the execution, e.g., `BuildArtifacts`.
:param task_name: A minor step/component of the process, e.g., AcrImageBuild.
:param periodic_logging: A boolean flag indicating if periodic logs should be printed 
                         for long-running tasks.
:param dynamic_logging: A boolean flag indicating if dynamic logging should be enabled.
                        If True, passes a logging closure to the decorated function.
"""


def log_monitor(service_name, process_name, task_name=None, periodic_logging=False, dynamic_logging=False, periodic_logging_interval=30):
    def get_step_info(service_name, step_name):
        config = load_process_config()
        process_steps = config.get(service_name, {})
        if not process_steps:
            raise ValueError(f"Service {service_name} not found.")

        step_order = process_steps.get(step_name)
        if step_order is None:
            return DEFAULT_PROGRESS

        total_steps = max(process_steps.values())  # 获取最大的步骤数作为总步数
        return f"{step_order}/{total_steps}"

    progress = get_step_info(service_name, process_name)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            global logging_thread, stop_thread
            logger = __get_inner_logger()
            extra = {'service_name': service_name, 'progress': progress}

            def log_message(message, error=False):
                if error:
                    logger.error(message, extra=extra)
                else:
                    logger.info(message, extra=extra)

            # 可供调用的闭包，用于被装饰的对象动态传入日志
            def dynamic_logging_message(message):
                logger.info(message, extra=extra)

            if dynamic_logging:
                kwargs[LOGGING_CLOSURE_NAME] = dynamic_logging_message

            def periodic_logging_task():
                if stop_thread:
                    while not stop_thread.is_set():
                        time.sleep(periodic_logging_interval)
                        if task_name:
                            logger.info(f"{task_name} is processing...", extra=extra)
                        else:
                            logger.info(f"{process_name} is processing...", extra=extra)

            try:

                if periodic_logging:
                    stop_thread = threading.Event()
                    logging_thread = threading.Thread(target=periodic_logging_task)
                    logging_thread.start()
                else:
                    stop_thread = None
                    logging_thread = None

                # 日志开始
                if task_name:
                    log_message(f"{process_name}-{task_name} Start!")
                else:
                    log_message(f"{process_name} Start!")
                logger.info("Processing...", extra=extra)
                result = func(*args, **kwargs)

                if logging_thread is not None:
                    stop_thread.set()
                    logging_thread.join()

                # 日志成功
                if task_name:
                    log_message(f"{process_name}-{task_name} Success!")
                else:
                    log_message(f"{process_name} Success!")

                return result
            except Exception as e:
                if logging_thread is not None:
                    stop_thread.set()
                    logging_thread.join()
                if task_name:
                    log_message(f"Error occurred in {process_name}-{task_name}\n"
                                f"{process_name}-{task_name} Failed!", error=True)
                else:
                    log_message(f"Error occurred in {process_name}\n"
                                f"{process_name} Failed!", error=True)

                raise CliCommonException(f"CLI has stopped running due to an error in {process_name}", original_exception=e) from e

        return wrapper

    return decorator
