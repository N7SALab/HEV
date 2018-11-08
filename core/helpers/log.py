import logging
from datetime import datetime


FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
FORMAT = '%(asctime)s [%(levelname)s ] %(message)s'
FORMAT = '[%(levelname)s ] %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)


def log(message, module=None):
    """ Default logging format

    """
    if not message:
        # logging.info('{} '.format(datetime.now().isoformat()))
        logging.info('')
    else:
        if module:
            # logging.info('{}  {}'.format(datetime.now().isoformat(), message))
            logging.info('[{}] {}'.format(module, message))
        else:
            logging.info('{}'.format(message))
