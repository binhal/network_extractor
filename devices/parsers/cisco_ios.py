"""
Parser implementation for Cisco IOS commands.
"""
import textfsm
from devices.parsers.base_parser import BaseParser

class CiscoIosParser(BaseParser):
    """
    Parser for Cisco IOS command outputs.
    """

    def parse(self, command_output):
        """
        Parses the raw command output using TextFSM.

        Args:
            command_output (str): The raw text output from a device command.

        Returns:
            dict: The structured data.
        """
        # This is a simplified example. In a real-world scenario, you would
        # have a TextFSM template for each command.
        # For demonstration, we'll do some basic parsing.

        # Example for 'show ip interface brief'
        if "Interface" in command_output and "IP-Address" in command_output:
            template = r"""Value Interface (\S+)
Value IP-Address (\S+)
Value Status (up|down|administratively down)
Value Protocol (up|down)

Start
  ^${Interface}\s+${IP-Address}\s+\w+\s+\w+\s+${Status}\s+${Protocol} -> Record"""
            fsm = textfsm.TextFSM(template)
            result = fsm.ParseText(command_output)
            return [dict(zip(fsm.header, row)) for row in result]

        # Example for 'show version'
        if "Cisco IOS Software" in command_output:
            for line in command_output.splitlines():
                if "Cisco IOS Software" in line:
                    return {"version": line.strip()}

        # Fallback for other commands
        return {"raw_output": command_output}
