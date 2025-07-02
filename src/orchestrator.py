"""
The main controller that orchestrates the workflow.
"""
import yaml
import json
from src.device_detector import detect_device_os
from src.device_connector import DeviceConnector
from src.output_parser import get_parser

class Orchestrator:
    """
    Orchestrates the device interaction workflow.
    """

    def __init__(self, command_file):
        """
        Initializes the Orchestrator.

        Args:
            command_file (str): Path to the YAML command file.
        """
        with open(command_file, 'r') as f:
            self.commands = yaml.safe_load(f)

    def execute(self, host, username, password):
        """
        Executes the full workflow for a device.

        Args:
            host (str): The IP address or hostname of the device.
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            str: A JSON string of the extracted device information.
        """
        # 1. Detect device OS
        device_os = detect_device_os(host, username, password)
        if not device_os:
            return json.dumps({"error": "Could not detect device OS"}, indent=4)

        print(f"Detected device OS: {device_os}")

        # 2. Get commands for the detected OS
        device_commands = self.commands.get(device_os)
        if not device_commands:
            return json.dumps({"error": f"No commands found for {device_os}"}, indent=4)

        # 3. Connect to the device with known device type
        connector = DeviceConnector(host, username, password, device_os)
        connection = connector.connect()
        if not connection:
            return json.dumps({"error": f"Failed to connect to {host}"}, indent=4)

        # 4. Get parser for the device
        parser = get_parser(device_os)
        if not parser:
            connector.disconnect()
            return json.dumps({"error": f"No parser found for {device_os}"}, indent=4)

        # 5. Execute commands and parse output
        device_data = {}
        for key, command in device_commands.items():
            print(f"Executing command: {command}")
            output = connector.send_command(command)
            if output:
                device_data[key] = parser.parse(output)
            else:
                device_data[key] = {"error": "Command execution failed"}

        # 6. Disconnect and return data
        connector.disconnect()
        return json.dumps(device_data, indent=4)
