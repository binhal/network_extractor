"""
An abstract base class for all parsers.
"""
from abc import ABC, abstractmethod

class BaseParser(ABC):
    """
    Abstract base class for command output parsers.
    """

    @abstractmethod
    def parse(self, command_output):
        """
        Parses the raw command output.

        Args:
            command_output (str): The raw text output from a device command.

        Returns:
            dict: The structured data.
        """
        pass
