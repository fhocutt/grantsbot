# FIXME DRY
def logrun(run_id, edited_pages, wrote_db, logged_errors):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    message = '\t%s\t%s\t%s\t%s' % (run_id, edited_pages, wrote_db,
                                    logged_errors)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler = logging.handlers.RotatingFileHandler('matchbot.log',
                                                   maxBytes=100,
                                                   backupCount=2)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(message)

# FIXME ditto
def logerror(message):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler = logging.FileHandler('matchbot_errors.log')
    logger.addHandler(handler)
    logger.error(message)

# TODO
def logmatch():
    pass

