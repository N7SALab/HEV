import logging

from logging import (CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG, NOTSET)


# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# WARN = WARNING
# INFO = 20
# DEBUG = 10
# NOTSET = 0


class hevlog:

    def __init__(self, name=None, level='info'):
        """ HEV logging class

        Centralizing all logging capabilities
        """

        # Set logger format
        # FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(module)s  %(message)s'
        # FORMAT = '[%(asctime)s][%(levelname)s ][%(threadName)s] [%(module)s] %(message)s'
        # FORMAT = '%(asctime)s [%(name)s] [%(levelname)s ] %(message)s'
        FORMAT = '%(asctime)s [%(levelname)s\t] [%(name)s] %(message)s'
        # FORMAT = '[%(name)s] [%(levelname)s ] %(message)s'
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
