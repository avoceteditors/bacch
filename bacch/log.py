
from sphinx.util.console import darkblue, darkgreen, brown, darkred
from sphinx.util.logging import getLogger

class BacchLogger:
    """Configures loging operations for Sphinx"""

    def init_logger(self):
        self.logger = getLogger(self.__class__.__name__)

    def debug(self, msg, nonl_val=False):
        self.logger.debug(darkblue(msg), nonl=nonl_val)

    def info(self, msg, nonl_val=False):
        self.logger.info(darkgreen(msg), nonl=nonl_val)

    def warn(self, msg, nonl_val=False):
        self.logger.warn(brown(msg), nonl=nonl_val)

    def critical(self, msg, nonl_val=False):
        self.logger.critical(darkred(msg), nonl=nonl_val)






