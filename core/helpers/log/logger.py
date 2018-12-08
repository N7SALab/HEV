import logging

from logging import INFO, DEBUG, WARNING, ERROR


class hevlog:

    def __init__(self, level='info'):
        """ HEV logging class

        Centralizing all logging capabilities
        """

        # Set logger format
        # FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
        # FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
        # FORMAT = '%(asctime)s [%(levelname)s ] %(message)s'
        FORMAT = '[%(levelname)s ] %(message)s'

        self.logging = logging
        if level.lower() == 'info':
            self.logging.basicConfig(format=FORMAT, level=INFO)
        if level.lower() == 'debug':
            self.logging.basicConfig(format=FORMAT, level=DEBUG)
        if level.lower() == 'warning':
            self.logging.basicConfig(format=FORMAT, level=WARNING)
        if level.lower() == 'error':
            self.logging.basicConfig(format=FORMAT, level=ERROR)
        self.INFO = INFO
        self.DEBUG = DEBUG
        self.ERROR = ERROR
        self.WARNING = WARNING

    def log(self, message=None, module=None, log_type=None):
        """ info, debug, error, warrning
        """
        if message is None:
            self.logging.info('')
        else:
            if log_type is not None:
                if log_type.lower() == 'info':
                    self.logging.info('[{}] {}'.format(module, message))
                if log_type.lower() == 'debug':
                    self.logging.debug('[{}] {}'.format(module, message))
                if log_type.lower() == 'error':
                    self.logging.error('[{}] {}'.format(module, message))
                if log_type.lower() == 'warning':
                    self.logging.warning('[{}] {}'.format(module, message))
            else:
                self.logging.info('{}'.format(message))
