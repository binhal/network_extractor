"""
Logic to detect the device OS.
"""
from src.device_connector import DeviceConnector


def detect_device_os(host, username, password):
    """
    Detects the device OS by connecting and running a command.

    Args:
        host (str): The IP address or hostname of the device.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The detected device OS (e.g., 'cisco_ios', 'juniper_junos').
    """
    # Use a generic device_type for initial connection
    generic_connector = DeviceConnector(host, username, password, 'autodetect')
    connection = generic_connector.connect()

    if connection:
        # Netmiko's autodetect should determine the device type
        device_type = connection.device_type
        generic_connector.disconnect()
        return device_type
    return None
