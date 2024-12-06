import logging
import traceback

from mip_utils.logging_formatter import CustomFormatter

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

class GeneralException(Exception):
    def __init__(self, msn: str, severity_level: logging):
        """
        General Exception class for the project.
        It deals with the severity level, and the logging of the exception.
        """
        self.msn = msn
        self.severity_level = severity_level

    def log(self, with_traceback=False):
        logging.log(self.severity_level, self.msn)
        if with_traceback:
            traceback_string = traceback.format_exc()
            print(traceback_string)


class InputDataError(GeneralException):
    """
    Raised whenever the input data is not valid.
    """


class SolutionError(GeneralException):
    """
    Raised when the output from the optimization or the output tables contain some problem.
    
    For example, if the solution is not feasible, or if the output from the optimization violates an expected
    constraint.
    """
