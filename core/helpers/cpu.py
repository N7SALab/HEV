import psutil

from core.helpers.logger import hevlog

hevlog = hevlog('cpu', level='debug')


def cpu_usage(self, max_cpu_percentage=80):
    """Limit max cpu usage
    """
    if psutil.cpu_percent() < max_cpu_percentage:
        hevlog.logging.debug('[cpu usage] {}%'.format(psutil.cpu_percent()))
        return True
    else:
        hevlog.logging.debug('[cpu usage] {}%'.format(psutil.cpu_percent()))
        return False
