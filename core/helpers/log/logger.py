import logging

from logging import (CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG, NOTSET)


class hevlog:

    def __init__(self, name=None, level='info'):
        """ HEV logging class

        Centralizing all logging capabilities
        """

        # Set logger format
        # FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
        # FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
        # FORMAT = '%(asctime)s [%(levelname)s ] %(message)s'
        FORMAT = '[%(name)s] [%(levelname)s ] %(message)s'
        # FORMAT = '[%(levelname)s ] [%(name)s] %(message)s'

        self.name = name
        self.level = self._level(level)

        self.logging = logging
        self.logging.basicConfig(format=FORMAT, level=self.level)
        self.logging = self.logging.getLogger(name)
        self.logging.setLevel(self.level)

    def _level(self, level):
        """ a way to set the level
        """
        if level is None:
            return INFO
        elif level.lower() == 'notset' or level.lower() == 'off':
            return NOTSET
        elif level.lower() == 'debug' or level.lower() == 'd':
            return DEBUG
        elif level.lower() == 'info' or level.lower() == 'i':
            return INFO
        elif level.lower() == 'warning' or level.lower() == 'w':
            return WARNING
        elif level.lower() == 'error' or level.lower() == 'e':
            return ERROR
        elif level.lower() == 'fatal' or level.lower() == 'f':
            return FATAL
        elif level.lower() == 'critical' or level.lower() == 'c':
            return CRITICAL
        else:
            return INFO

    def set_level(self, level):
        return self.logging.setLevel(self._level(level))

    def log(self, message, module, log_type):
        """ info, debug, error, warrning
        """

        log_level = self._level(log_type)

        if message is None or not message:
            return self.logging.info('')
        else:
            if module and log_type:
                if log_type.lower() == 'info' and log_level >= self.level:
                    return self.logging.info('[{}] {}'.format(module, message))
                
                if log_type.lower() == 'debug' and log_level >= self.level:
                    return self.logging.debug('[{}] {}'.format(module, message))

                if log_type.lower() == 'error' and log_level >= self.level:
                    return self.logging.error('[{}] {}'.format(module, message))

                if log_type.lower() == 'warning' and log_level >= self.level:
                    return self.logging.warning('[{}] {}'.format(module, message))

                if log_type.lower() == 'fatal' and log_level >= self.level:
                    return self.logging.fatal('[{}] {}'.format(module, message))

            if log_type:
                if log_type.lower() == 'info' and log_level >= self.level:
                    return self.logging.info('{}'.format(message))

                if log_type.lower() == 'debug' and log_level >= self.level:
                    return self.logging.debug('{}'.format(message))

                if log_type.lower() == 'error' and log_level >= self.level:
                    return self.logging.error('{}'.format(message))

                if log_type.lower() == 'warning' and log_level >= self.level:
                    return self.logging.warning('{}'.format(message))

            if module and not log_type:
                return self.logging.info('[{}] {}'.format(module, message))

            if not module and not log_type:
                return self.logging.info('{}'.format(message))
