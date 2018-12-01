import logging

from logging import INFO, DEBUG, ERROR, WARNING


# Set logger format
# FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
# FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
# FORMAT = '%(asctime)s [%(levelname)s ] %(message)s'
FORMAT = '[%(levelname)s ] %(message)s'

# TODO: need to find out which logging config is used when there are multiple ones
logging.basicConfig(format=FORMAT, level=DEBUG)


def log(message=None, module=None, log_type=None):
    """ Default logging

    """
    if not message:
        logging.info('')
    else:
        if module:
            if log_type is INFO:
                logging.info('[{}] {}'.format(module, message))
            if log_type is DEBUG:
                logging.debug('[{}] {}'.format(module, message))
            if log_type is ERROR:
                logging.error('[{}] {}'.format(module, message))
            if log_type is WARNING:
                logging.warning('[{}] {}'.format(module, message))
        else:
            logging.info('{}'.format(message))


def hevlog(message=None, module=None, log_type=None):
    """ Default HEV logging

    """
    if not message:
        logging.info('')
    else:
        if module:
            if log_type is INFO:
                logging.info('[{}] {}'.format(module, message))
            if log_type is DEBUG:
                logging.debug('[{}] {}'.format(module, message))
            if log_type is ERROR:
                logging.error('[{}] {}'.format(module, message))
            if log_type is WARNING:
                logging.warning('[{}] {}'.format(module, message))
        else:
            logging.info('{}'.format(message))
