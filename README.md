# NASA 1995 HTTP Log Analyzer

This is a log analyzer tool designed to process the NASA HTTP Logs from 1995.  
The tool parses the raw HTTP access logs and categorizes the entries based on:

- Host (client making the request)
- HTTP request
- HTTP response status code

The analyzer also identifies useful statistics such as:

- Most active hosts
- Most requested files
- Most common HTTP status codes

These metrics help provide insights into traffic patterns and server activity within the NASA web server logs.

---

## Requirements

- Python 3

---

## Usage

Run the script from the terminal using the following command:

```bash
python3 log.py <path_to_log_file>
