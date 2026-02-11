# Build Log Scanner (`scan_last.py`)

A specialized Python utility for DevOps/SREs to quickly inspect the tail of build logs on remote servers. 

This script connects via UNC paths, reads the last 500 lines of the `build.log` file, and flags any occurrences of **ERROR** or **FAILURE**, providing the immediate context for debugging.

## Features
- **Targeted Scanning:** hardcoded to check `\\<server>\temp\log\build.log`.
- **Efficient Reading:** Uses `collections.deque` to read only the last 500 lines, avoiding memory issues with large log files.
- **Context Awareness:** Prints the error line plus the following 2 lines to give context to the alert.
- **Robust Encoding:** Handles ASCII decoding and re-encoding to safely check for error keywords in binary or mixed-content logs.

## Prerequisites
- **Python 3.x**
- **Network Access:** You must have access to the target server's file shares.
- **Read Permissions:** Your user account must have read permissions on the `\temp\log\` directory of the target machine.

## Installation

1. Save the script as `scan_last.py`.
2. Ensure you can reach the remote servers via Windows Explorer or command line.

## Usage

Run the script from your terminal or command prompt, passing the **server name** as an argument.

```bash
python scan_last.py <server_name>
