"""
Logic to detect the device OS.
"""
from netmiko.ssh_autodetect import SSHDetect
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException


def detect_device_os(host, username, password):
    """
    Detects the device OS by using Netmiko's autodetection capability.

    Args:
        host (str): The IP address or hostname of the device.
        username (str): The username for authentication.
        password (str): The password for authentication.

    Returns:
        str: The detected device OS (e.g., 'cisco_ios', 'juniper_junos') or None if detection fails.
    """
    try:
        # Create device dictionary for SSHDetect
        remote_device = {
            'device_type': 'autodetect',
            'host': host,
            'username': username,
            'password': password
        }
        
        # Use SSHDetect for autodetection
        guesser = SSHDetect(**remote_device)
        best_match = guesser.autodetect()
        
        return best_match
        
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Error detecting device OS for {host}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during device detection for {host}: {e}")
        return None
