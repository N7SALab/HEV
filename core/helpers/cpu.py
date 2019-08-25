import psutil

from core.helpers.hevlog import Hevlog

hevlog = Hevlog('cpu', level='debug')


def cpu_usage(self, max_cpu_percentage=80):
    """Limit max cpu usage
    """
    if psutil.cpu_percent() < max_cpu_percentage:
        Hevlog.logging.debug('[cpu usage] {}%'.format(psutil.cpu_percent()))
        return True
    else:
        Hevlog.logging.debug('[cpu usage] {}%'.format(psutil.cpu_percent()))
        return False
