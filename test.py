import log

logger = log.logging()
logger.setLevel(log.logging.DEBUG)
logger.set_format_setting(indent=1, width=50)

logger.debug("debug")
logger.info("info")
logger.warning("warning")
logger.error("error")
logger.critical("critical")
