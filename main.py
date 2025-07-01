
"""
Main entry point of the application.
"""
import os
import argparse
from src.orchestrator import Orchestrator

def main():
    """
    Main function to run the network extractor.
    """
    parser = argparse.ArgumentParser(description="Network Device Information Extractor")
    parser.add_argument("--host", required=True, help="Device IP or hostname")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")
    args = parser.parse_args()

    # Get the absolute path to the commands.yaml file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    command_file = os.path.join(script_dir, 'commands.yaml')

    orchestrator = Orchestrator(command_file)
    result = orchestrator.execute(args.host, args.username, args.password)

    print("\n--- Extracted Information ---")
    print(result)
    print("---------------------------")

if __name__ == "__main__":
    main()
