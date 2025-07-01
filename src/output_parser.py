"""
Contains parsing logic for different command outputs.
"""
from devices.parsers.cisco_ios import CiscoIosParser
from devices.parsers.juniper_junos import JuniperJunosParser

# Add other parsers here as you support more vendors

PARSERS = {
    "cisco_ios": CiscoIosParser(),
    "juniper_junos": JuniperJunosParser(),
    # 'arista_eos': AristaEosParser(), # Example for another vendor
}

def get_parser(device_type):
    """
    Returns the appropriate parser for the given device type.

    Args:
        device_type (str): The device OS type.

    Returns:
        An instance of a parser class.
    """
    return PARSERS.get(device_type)
