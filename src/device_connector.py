"""
Handles SSH/API connection logic.
"""
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

class DeviceConnector:
    """
    A class to manage connections to network devices.
    """

    def __init__(self, host, username, password, device_type):
        """
        Initializes the DeviceConnector.

        Args:
            host (str): The IP address or hostname of the device.
            username (str): The username for authentication.
            password (str): The password for authentication.
            device_type (str): The Netmiko device type.
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