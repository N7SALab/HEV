import logging
from datetime import datetime


FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def log(message):
    """ Default logging format

    """
    if not message:
        # logging.info('{} '.format(datetime.now().isoformat()))
        logging.info('')
    else:
        # logging.info('{}  {}'.format(datetime.now().isoformat(), message))
        logging.info('{}'.format(message))
