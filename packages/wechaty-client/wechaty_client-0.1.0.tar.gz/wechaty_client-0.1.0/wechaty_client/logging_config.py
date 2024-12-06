import logging.config
import os

# 清除之前已存在的日志记录器，防止其他依赖模块有自己的logger
logging.getLogger().handlers.clear()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s-%(filename)s-%(levelname)s-'%(message)s'",
        },
        "detailed": {
            "format": "%(asctime)s-%(levelname)s-[%(filename)s:%(lineno)d]-'%(message)s'",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
        },
        "file_debug": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": f"{log_dir}/debug.log",
            "level": "DEBUG",
            # 5MB
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
        "file_error": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": f"{log_dir}/error.log",
            "level": "ERROR",
            # 5MB
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
    },
    "loggers": {
        "default": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "custom": {
            "handlers": ["console", "file_error"],
            "level": "ERROR",
            "propagate": False,
        },
    }
}

logging.config.dictConfig(logging_config)