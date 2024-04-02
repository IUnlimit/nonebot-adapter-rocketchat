from nonebot.utils import logger_wrapper

log = logger_wrapper("RocketChat")

def debug(text: str, e: Exception):
    log("DEBUG", text, e)

def success(text: str):
    log("SUCCESS", text)

def info(text: str):
    log("INFO", text)

def error(text: str, e: Exception):
    log("ERROR", text, e)