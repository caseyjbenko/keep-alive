# Keep-Alive Service

This project, titled "Keep-Alive", is designed to manage and wake devices on a network using Wake-on-LAN (WoL) packets. It features a Python script that can either be run as a command-line tool or as a systemd service for continuous monitoring.

## Features

- **Status Checking**: Check the online/offline status of all devices in the database.
- **Manual/Automatic Wake**: Manually wake devices or automatically wake them based on specified tags.
- **Database Management**: Add, update, list, and remove devices from the database.
- **Continuous Monitoring**: Monitor specific devices and send WoL packets if they are found to be offline.

## Prerequisites

- Python 3
- `wakeonlan` Python package

## Installation

1. **Clone the Repository**:
   

   ```bash
   git clone [https://github.com/caseyjbenko/keep-alive.git]
   cd [keep-alive]
   ```

2. **Install Dependencies**:

   Run the provided script to install the required Python packages.

   ```bash
   python3 install_dependencies.py
   ```

3. **Initialize the Database**:

   Use this command to create the SQLite database file and the necessary table.

   ```bash
   python3 create_database.py
   ```

## Usage

Execute the script with the following structure:

```bash
python3 script.py [command] [arguments]
```

### Commands

- `status`: Checks the status of all devices.
- `wake [tag,...]`: Wakes up devices associated with the specified tags.
- `monitor [tag,...]`: Continuously monitors and wakes devices with specific tags.
- `list`: Lists all devices in the database.
- `upsert <ip> <mac> <tag>`: Adds or updates a device in the database.
- `remove <ip>`: Removes a device from the database.

### Examples

- Check the status of all devices:

  ```bash
  python3 script.py status
  ```

- Wake up all devices with a specific tag:

  ```bash
  python3 script.py wake office
  ```

- Continuously monitor devices with a specific tag:

  ```bash
  python3 script.py monitor server
  ```

## Setting Up as a Systemd Service

To run the script as a systemd service for continuous monitoring:

1. **Create a Bash Script (`keep_alive_service.sh`)**:

   Include the following content, modifying the path to the Python script and the tag as needed.

   ```bash
   #!/bin/bash
   /usr/bin/python3 /path/to/script.py monitor [tag]
   ```

2. **Create a Systemd Service File (`keep-alive.service`)**:

   Place this file in `/etc/systemd/system/`.

   ```ini
   [Unit]
   Description=Keep-Alive Monitoring Service

   [Service]
   ExecStart=/path/to/keep_alive_service.sh
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and Start the Service**:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable keep-alive.service
   sudo systemctl start keep-alive.service
   ```

4. **Check the Service Status**:

   ```bash
   sudo systemctl status keep-alive.service
   ```

## License

MIT

