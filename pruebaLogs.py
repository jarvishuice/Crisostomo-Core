from logging import getLogger

def execute():
    logger = getLogger("AppLogger")
    logger.info("Probvando el logger")
    return 0