"""
Handles SSH/API connection logic.
"""
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

class DeviceConnector:
    """
    A class to manage connections to network devices.
    """

    def __init__(self, host, username, password, device_type=None):
        """
        Initializes the DeviceConnector.

        Args:
            host (str): The IP address or hostname of the device.
            username (str): The username for authentication.
            password (str): The password for authentication.
            device_type (str, optional): The Netmiko device type. If None, autodetection will be used.
        """
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type
        self.connection = None

    def connect(self):
        """
        Establishes an SSH connection to the device.
        """
        try:
            # If no device_type is set, try autodetection
            if not self.device_type:
                from .device_detector import detect_device_os
                detected_type = detect_device_os(self.host, self.username, self.password)
                if not detected_type:
                    print(f"Could not autodetect device type for {self.host}")
                    return None
                self.device_type = detected_type
            
            self.connection = ConnectHandler(
                device_type=self.device_type,
                host=self.host,
                username=self.username,
                password=self.password,
            )
            return self.connection
        except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
            print(f"Error connecting to {self.host}: {e}")
            return None

    def disconnect(self):
        """
        Closes the SSH connection.
        """
        if self.connection:
            self.connection.disconnect()

    def send_command(self, command):
        """
        Sends a command to the device and returns the output.

        Args:
            command (str): The command to execute.

        Returns:
            str: The raw output of the command.
        """
        if self.connection:
            return self.connection.send_command(command)
        return None