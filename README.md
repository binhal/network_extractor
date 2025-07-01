# Network Device Information Extractor

This system is a modular and extensible Python application designed to connect to network devices, detect their operating system, execute predefined commands, and return structured data.

## Core Features

- **Auto-Detects Device Type:** Automatically determines the device OS (e.g., `cisco_ios`, `juniper_junos`) using SSH.
- **Configuration-Driven:** Uses a `commands.yaml` file to map device types to the specific commands needed to retrieve information.
- **Modular Architecture:** Separates concerns for connection, detection, and parsing, making it easy to extend.
- **Structured Output:** Parses raw command output into structured JSON using TextFSM templates.

---

## Project Structure

```
network_extractor/
│
├── main.py                 # Main entry point (accepts CLI arguments).
├── README.md               # This documentation file.
├── requirements.txt        # Project dependencies.
├── commands.yaml           # Defines commands for each device OS.
├── venv/                   # Python virtual environment.
│
├── src/
│   ├── __init__.py
│   ├── device_connector.py   # Handles SSH connection logic.
│   ├── device_detector.py    # Logic to detect the device OS.
│   ├── output_parser.py      # Factory for getting the correct parser.
│   └── orchestrator.py       # Main controller that runs the workflow.
│
└── devices/
    └── parsers/
        ├── base_parser.py    # Abstract base class for all parsers.
        ├── cisco_ios.py      # Parser implementation for Cisco IOS.
        └── juniper_junos.py  # Parser implementation for Juniper Junos.
```

---

## Setup and Installation

1.  **Create Virtual Environment:**
    The project requires a virtual environment. One has already been created at `network_extractor/venv/`.

2.  **Install Dependencies:**
    The required Python packages have already been installed into the virtual environment. If you need to reinstall them, run:
    ```bash
    network_extractor/venv/bin/pip install -r network_extractor/requirements.txt
    ```

---

## How to Run

The application is run from the command line, providing the target device's information as arguments.

**Command:**
```bash
/home/leanb/network_infomation_extractor/network_extractor/venv/bin/python /home/leanb/network_infomation_extractor/network_extractor/main.py --host <DEVICE_IP> --username <USERNAME> --password <PASSWORD>
```

**Example:**
```bash
/home/leanb/network_infomation_extractor/network_extractor/venv/bin/python /home/leanb/network_infomation_extractor/network_extractor/main.py --host 192.168.1.1 --username admin --password mysecretpassword
```

---

## Extending the System

### Adding a New Device OS

1.  **Update `commands.yaml`:** Add a new top-level key for the new OS (e.g., `arista_eos`) and define the commands to run.
    ```yaml
    arista_eos:
      get_hostname: "show running-config | include hostname"
      get_version: "show version"
      # ... etc
    ```

2.  **Create a New Parser:**
    - Create a new file in `devices/parsers/`, for example `arista_eos.py`.
    - Inside, create a class that inherits from `BaseParser` (e.g., `AristaEosParser`).
    - Implement the `parse` method with logic (ideally TextFSM templates) to handle the output from the commands you defined.

3.  **Register the Parser:**
    - In `src/output_parser.py`, import your new parser class.
    - Add it to the `PARSERS` dictionary, mapping the OS key to an instance of your new parser class.
    ```python
    # src/output_parser.py
    from devices.parsers.arista_eos import AristaEosParser

    PARSERS = {
        "cisco_ios": CiscoIosParser(),
        "juniper_junos": JuniperJunosParser(),
        "arista_eos": AristaEosParser(), # Add the new parser here
    }
    ```

### Improving Parsers

The current parsers are very basic. To make them useful, you should create robust [TextFSM templates](https://github.com/google/textfsm) for each command defined in `commands.yaml` and implement the logic in the respective parser class.
