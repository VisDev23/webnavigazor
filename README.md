# WebNavigazor

WebNavigazor is a Python-based web enumeration tool that performs directory and subdomain enumeration. It introduces random delays between requests to avoid detection and logs the results to files. This tool can be used to discover subdomains, directories, and gather web server details of a target domain.

## Features

- Subdomain enumeration
- Directory enumeration
- Random delays between requests to avoid detection
- Option to use HTTPS for directory enumeration
- Logging results to files
- Fetching web server details

## Requirements

- Python 3.x
- Required Python libraries: `requests`, `dnspython`, `concurrent.futures`

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/VisDev23/webnavigazor.git
   cd webnavigazor
   ```

2. Install the required libraries:

   ```sh
   pip install -r requirements.txt
   ```


## Usage

    ```sh
python WebNavigazor.py <domain> <subdomain_list> <directory_list> [-H] [-min <min_delay>] [-max <max_delay>] [-o <output_prefix>]
    ```

### Arguments

- `domain`: Target domain for enumeration
- `subdomain_list`: File containing subdomains list
- `directory_list`: File containing directories list

### Optional Arguments

- `-H`, `--https`: Use HTTPS for directory enumeration (optional)
- `-min`, `--min_delay`: Minimum delay between requests in seconds (default: 0.5)
- `-max`, `--max_delay`: Maximum delay between requests in seconds (default: 3.0)
- `-o`, `--output_prefix`: Prefix for output folder and files (optional)

### Example

   ```sh
python WebNavigazor.py example.com subdomains.txt directories.txt -H -min 0.3 -max 2.0 -o results
   ```

## Output

- Subdomain enumeration results are saved in `subdomains.txt` in the output folder.
- Directory enumeration results are saved in `directories.txt` in the output folder.
- Web server details are saved in `webserver_details.txt` in the output folder.

## Creator Information

```
Creator: Vis Dev & Manjima V
```

## ASCII Art

```
░██╗░░░░░░░██╗███████╗██████╗░███╗░░██╗░█████╗░██╗░░░██╗██╗░██████╗░░█████╗░███████╗░█████╗░██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗████╗░██║██╔══██╗██║░░░██║██║██╔════╝░██╔══██╗╚════██║██╔══██╗██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝██╔██╗██║███████║╚██╗░██╔╝██║██║░░██╗░███████║░░███╔═╝██║░░██║██████╔╝
░░████╔═████║░██╔══╝░░██╔══██╗██║╚████║██╔══██║░╚████╔╝░██║██║░░╚██╗██╔══██║██╔══╝░░██║░░██║██╔══██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░╚███║██║░░██║░░╚██╔╝░░██║╚██████╔╝██║░░██║███████╗╚█████╔╝██║░░██║
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚═════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝
```
```
# webnavigazor
