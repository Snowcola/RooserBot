import os
import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[2;1m"
    cyan = "\x1b[36;1m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    COLOR_MAP = {
        logging.DEBUG: grey,
        logging.INFO: cyan,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }

    @classmethod
    def colorize(cls, color):
        return f"%(asctime)s {color}|%(levelname)s|{cls.reset} %(name)s: %(message)s"

    def format(self, record):
        log_fmt = self.colorize(self.COLOR_MAP.get(record.levelno))
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "error": logging.ERROR,
    "warning": logging.WARNING,
    "warn": logging.WARN,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL,
}

DISCORD_LOG_LEVEL = levels[os.environ.get("DISCORD_LOG_LEVEL", "error")]
BOT_LOG_LEVEL = levels[os.environ.get("BOT_LOG_LEVEL", "info")]

formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Discord.py logger
disc_logger = logging.getLogger("discord")
disc_logger.setLevel(DISCORD_LOG_LEVEL)
handler = logging.FileHandler(filename="/app/logs/discord.log", encoding="utf-8", mode="w")
handler.setFormatter(formatter)
disc_logger.addHandler(handler)

# RoosterBot logger
logger = logging.getLogger("RoosterBot")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(CustomFormatter())
stream_handler.setLevel(BOT_LOG_LEVEL)
logger.addHandler(stream_handler)
logger.setLevel(BOT_LOG_LEVEL)

# YoutubeDL Logger
ytdl_logger = logging.getLogger("youtube-dl")
ytdl_stream_handler = logging.StreamHandler()
ytdl_stream_handler.setFormatter(CustomFormatter())
ytdl_stream_handler.setLevel(BOT_LOG_LEVEL)
ytdl_logger.setLevel(BOT_LOG_LEVEL)
ytdl_logger.addHandler(ytdl_stream_handler)
