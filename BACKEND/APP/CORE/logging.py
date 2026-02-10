import logging
import sys

def setup_logging():
    """
    CONFIGURES THE ROOT LOGGER FOR THE APPLICATION.
    SETS FORMAT TO: [TIME] [LEVEL] [MODULE]: MESSAGE
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # SILENCE NOISY LIBRARIES IF NEEDED
    logging.getLogger("multipart").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    logger = logging.getLogger("face_enhancer")
    logger.info("LOGGING CONFIGURED SUCCESSFULLY.")
    return logger

logger = setup_logging()