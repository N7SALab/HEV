import logging

from logging import INFO, DEBUG, WARNING, ERROR


# Set logger format
# FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
# FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
# FORMAT = '%(asctime)s [%(levelname)s ] %(message)s'
FORMAT = '[%(levelname)s ] %(message)s'


# def log(message=None, module=None, log_type=None):
#     """ Default logging
#
#     """
#     if not message:
#         logging.info('')
#     else:
#         if module:
#             if log_type is INFO:
#                 logging.info('[{}] {}'.format(module, message))
#             if log_type is DEBUG:
#                 logging.debug('[{}] {}'.format(module, message))
#             if log_type is ERROR:
#                 logging.error('[{}] {}'.format(module, message))
#             if log_type is WARNING:
#                 logging.warning('[{}] {}'.format(module, message))
#         else:
#             logging.info('{}'.format(message))


# def hevlog(message=None, module=None, log_type=None):
#     """ Default HEV logging
#
#     """
#     if not message:
#         logging.info('')
#     else:
#         if module:
#             if log_type is INFO:
#                 logging.info('[{}] {}'.format(module, message))
#             if log_type is DEBUG:
#                 logging.debug('[{}] {}'.format(module, message))
#             if log_type is ERROR:
#                 logging.error('[{}] {}'.format(module, message))
#             if log_type is WARNING:
#                 logging.warning('[{}] {}'.format(module, message))
#         else:
#             logging.info('{}'.format(message))


class hevlog:

    def __init__(self, level='info'):
        self.logging = logging
        self.format = '[%(levelname)s ] %(message)s'
        if level.lower() == 'info':
            self.logging.basicConfig(format=self.format, level=INFO)
        if level.lower() == 'debug':
            self.logging.basicConfig(format=self.format, level=DEBUG)
        if level.lower() == 'warning':
            self.logging.basicConfig(format=self.format, level=WARNING)
        if level.lower() == 'error':
            self.logging.basicConfig(format=self.format, level=ERROR)
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
