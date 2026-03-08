"""

This is a log analyzer tool designed to process the NASA HTTP Logs from 1995.
The tool aims to categorize the logs based on host, HTTM request, and HTTP reply status.
Likewise, it will also try to identify the most active hosts, the most requested files, and the most common HTTP status codes.

To run, type the following command in the terminal: 

python3 log.py <path_to_log_file>

Make sure that the log file is in the same directory as this script or provide the correct path to the log file.

Developed by: Luis Angelo Viloria (lpviloria@up.edu.ph) (langeloviloria@gmail.com)
Date Created: 16 February 2026
Last Updated: 09 March 2026

"""

from collections import Counter
import sys

if len(sys.argv) != 2:
    print("Usage: python3 log.py <path_to_log_file>")
    sys.exit(1)

file_path = sys.argv[1]
host_count = Counter()
request_count = Counter()
status_count = Counter()
file_type_count = Counter()
directory_count = Counter()
error_rate = 0

"""

The access logs are structured in the following format:
host - - [date:time] "request" status bytes

This makes parsing the logs straightforward, as we can split each line into its components and extract the relevant information for analysis.
However, keep in my the logs aren't stored in a structured format like JSON or CSV, so we need to be careful when parsing 
to ensure we correctly handle any irregularities in the log entries. Python opens files as UTF-8 by default, but due to how old the log files are,
it can be assumed that either the format is not UTF-8 or there are some malformed entries. To handle this, 
we can specify the encoding and error handling when opening the file.

When you browse through the log files, you might notice that one of the status codes is either '<berend@blazemonger.pc.cc.cmu.edu>', '5866', or just '"'.
These are not valid HTTP status codes and are likely the result of malformed log entries. To handle this, 
we can simply ignore any entries that do not conform to the expected format when parsing the logs. 
This way, we can ensure that our analysis is based on valid data and avoid any potential issues caused by malformed entries.

"""
try:
    f = open(file_path, 'r', encoding='utf-8', errors='ignore')
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found. Make sure that the log file is in the correct directory and provide the correct path.")
    sys.exit(1)

for line in f:
    parts = line.split()

    if len(parts) < 9:
        continue  # Skip malformed entries

    host = parts[0]
    request = parts[6]  # The requested file is usually the 7th element in the log entry
    extension = request.split('.')[-1] if '.' in request else 'Unknown file type'
    extension_to_store = extension.upper()

    status = parts[8]   # The status code is usually the 9th element in the log entry
    check_status = (int)(status) if status.isdigit() else None

    if check_status is None or check_status < 100 or check_status > 599:
        continue 

    error_rate += 1 if check_status >= 400 else 0

    host_count[host] += 1
    request_count[request] += 1
    status_count[status] += 1
    file_type_count[extension_to_store] += 1
    
"""

Now we have Counter objects that contain the counts for hosts, requests, and status codes. 
We can use the most_common() method of the Counter class to get the most active hosts, the most requested files, 
and the most common HTTP status codes. We can do a quick sanity check to see the top 10 entries from each category.
Just uncomment the section below to see the results.

"""

# print("Top 10 Active Hosts: ", host_count.most_common(10))
# print("Top 10 Requested Files: ", request_count.most_common(10))
# print("Top 10 HTTP Status Codes: ", status_count.most_common(10))

"""

Now that we have the most common entries, we can also calculate the total number of unique hosts, unique requests, and unique status codes.

"""

most_common_entries = {
    'hosts': host_count.most_common(10),
    'requests': request_count.most_common(10),
    'status_codes': status_count.most_common(10)
}

top_3_file_types = file_type_count.most_common(3)

total_unique_hosts = len(host_count)
total_unique_requests = len(request_count)
total_unique_status_codes = len(status_count)

"""

It would be ideal to present the results in a more readable format. Since this is ran in the terminal,
we can just do basic formatting to display the results in a clear and concise manner.

TODO:   Consider implementing a more advanced visualization of the results, such as using a library 
        like matplotlib to create bar charts or pie charts for the most common entries.

"""

print(f"\nError Rate: {error_rate/request_count.total() * 100 :.2f}% errors from total requests")

print("\nMost Common Entries:")
for category, entries in most_common_entries.items():
    print(f"\n{category.capitalize()}:")
    for entry, count in entries:
        print(f"{entry}: {count}")
print(f"\nTotal Unique Hosts: {total_unique_hosts}")
print(f"Total Unique Requests: {total_unique_requests}")
print(f"Total Unique HTTP Status Codes: {total_unique_status_codes}")
print("\nTop 3 Common File Types")
for file_type, count in top_3_file_types:
    print(f"{file_type}: {count/file_type_count.total() * 100:.2f}%")