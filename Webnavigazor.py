import os
import requests
import dns.resolver
import concurrent.futures
import random
import time
import argparse
import logging

# ASCII Art for WebNavigazor
ASCII_ART = """
░██╗░░░░░░░██╗███████╗██████╗░███╗░░██╗░█████╗░██╗░░░██╗██╗░██████╗░░█████╗░███████╗░█████╗░██████╗░
░██║░░██╗░░██║██╔════╝██╔══██╗████╗░██║██╔══██╗██║░░░██║██║██╔════╝░██╔══██╗╚════██║██╔══██╗██╔══██╗
░╚██╗████╗██╔╝█████╗░░██████╦╝██╔██╗██║███████║╚██╗░██╔╝██║██║░░██╗░███████║░░███╔═╝██║░░██║██████╔╝
░░████╔═████║░██╔══╝░░██╔══██╗██║╚████║██╔══██║░╚████╔╝░██║██║░░╚██╗██╔══██║██╔══╝░░██║░░██║██╔══██╗
░░╚██╔╝░╚██╔╝░███████╗██████╦╝██║░╚███║██║░░██║░░╚██╔╝░░██║╚██████╔╝██║░░██║███████╗╚█████╔╝██║░░██║
░░░╚═╝░░░╚═╝░░╚══════╝╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚═════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝
"""
CREATOR_INFO = "Creator: Vis Dev & Manjima V"
HOW_TO_USE = """
======================
     How to Use
======================
1. Required arguments:
   - domain: Target domain for enumeration
   - subdomain_list: File containing subdomains list
   - directory_list: File containing directories list
   
2. Optional arguments:
   -H, --https: Use HTTPS for directory enumeration (optional)
   -min, --min_delay: Minimum delay between requests in seconds (default: 0.5)
   -max, --max_delay: Maximum delay between requests in seconds (default: 3.0)
   -o, --output_prefix: Prefix for output folder and files (optional)

3. Example usage:
   python WebNavigazor.py example.com subdomains.txt directories.txt -H -min 0.3 -max 2.0 -o results

4. Required Libraries:
   - requests
   - dnspython
   - concurrent.futures
"""

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_libraries():
    try:
        import requests
        import dns.resolver
        import concurrent.futures
        return True
    except ImportError:
        return False

def create_output_folder(output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        logging.info(f"Created output folder: {output_folder}")

def enumerate_subdomains(domain, subdomain_list, min_delay, max_delay, output_file):
    found_subdomains = []
    with open(subdomain_list, 'r') as file:
        for subdomain in file:
            subdomain = subdomain.strip()
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = dns.resolver.resolve(full_domain, 'A')
                found_subdomains.append(full_domain)
                logging.info(f"Subdomain found: {full_domain} -> IP: {[str(i) for i in ip]}")
                # Check status code of the subdomain
                status_code = get_status_code(f"http://{full_domain}")
                if status_code is not None:
                    logging.info(f"Subdomain status: {full_domain} [Status Code: {status_code}]")
                # Write the result to the output file
                with open(output_file, 'a') as out_file:
                    out_file.write(f"Subdomain found: {full_domain} -> IP: {[str(i) for i in ip]} [Status Code: {status_code}]\n")
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
                pass
            # Introduce random delay to avoid detection
            delay = random.uniform(min_delay, max_delay)
            logging.info(f"Sleeping for {delay:.2f} seconds")
            time.sleep(delay)
    return found_subdomains

def get_status_code(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code
    except requests.RequestException:
        return None

def check_url(url, min_delay, max_delay, output_file):
    status_code = get_status_code(url)
    if status_code in [200, 403, 401]:
        logging.info(f"Found: {url} [Status Code: {status_code}]")
        with open(output_file, 'a') as out_file:
            out_file.write(f"Directory found: {url} [Status Code: {status_code}]\n")
        return url
    # Introduce random delay to avoid detection
    delay = random.uniform(min_delay, max_delay)
    logging.info(f"Sleeping for {delay:.2f} seconds")
    time.sleep(delay)
    return None

def enumerate_directories(domain, directory_list, protocol, min_delay, max_delay, output_file):
    found_directories = []
    with open(directory_list, 'r') as file:
        urls = [f"{protocol}://{domain}/{directory.strip()}" for directory in file]
        
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_url, url, min_delay, max_delay, output_file): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                found_directories.append(result)
    return found_directories

def get_webserver_details(url, output_file):
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        server_details = {
            'Server': headers.get('Server', 'Not Found'),
            'Content-Type': headers.get('Content-Type', 'Not Found'),
            'Headers': dict(headers)
        }
        
        # Write the server details to the output file
        with open(output_file, 'a') as out_file:
            out_file.write(f"Webserver details for {url}:\n{server_details}\n\n")
        
        logging.info(f"Webserver details: {server_details}")
        return server_details
    except requests.RequestException as e:
        error_message = {'Error': str(e)}
        
        # Write the error to the output file
        with open(output_file, 'a') as out_file:
            out_file.write(f"Error fetching webserver details for {url}: {error_message}\n")
        
        logging.error(f"Error fetching webserver details: {error_message}")
        return error_message

def main(domain, subdomain_list, directory_list, use_https, min_delay, max_delay, output_prefix):
    protocol = 'https' if use_https else 'http'

    # Check if required libraries are installed
    if not check_libraries():
        print("Error: Required libraries are not installed. Please install requests, dnspython, and concurrent.futures libraries.")
        return

    # Display ASCII Art and creator info
    print(ASCII_ART)
    print(CREATOR_INFO)
    print(HOW_TO_USE)

    # Create output folder
    output_folder = f"{output_prefix}_{domain}" if output_prefix else f"results_{domain}"
    create_output_folder(output_folder)

    subdomain_output = os.path.join(output_folder, "subdomains.txt")
    directory_output = os.path.join(output_folder, "directories.txt")
    webserver_output = os.path.join(output_folder, "webserver_details.txt")
    
    logging.info(f"Enumerating subdomains for {domain}...")
    enumerate_subdomains(domain, subdomain_list, min_delay, max_delay, subdomain_output)
    logging.info(f"Subdomain enumeration complete. Results written to {subdomain_output}.")
    
    logging.info(f"Enumerating directories for {domain} using {protocol}...")
    enumerate_directories(domain, directory_list, protocol, min_delay, max_delay, directory_output)
    logging.info(f"Directory enumeration complete. Results written to {directory_output}.")
    
    logging.info(f"Fetching webserver details for {domain}...")
    get_webserver_details(f"{protocol}://{domain}", webserver_output)
    logging.info(f"Webserver details fetched. Results written to {webserver_output}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web enumeration tool with random delay and file output")
    parser.add_argument("domain", help="Target domain for enumeration")
    parser.add_argument("subdomain_list", help="File containing subdomains list")
    parser.add_argument("directory_list", help="File containing directories list")
    parser.add_argument("-H", "--https", action="store_true", help="Use HTTPS for directory enumeration")
    parser.add_argument("-min", "--min_delay", type=float, default=0.5, help="Minimum delay between requests in seconds")
    parser.add_argument("-max", "--max_delay", type=float, default=3.0, help="Maximum delay between requests in seconds")
    parser.add_argument("-o", "--output_prefix", default="", help="Prefix for output folder and files")

    args = parser.parse_args()
    main(args.domain, args.subdomain_list, args.directory_list, args.https, args.min_delay, args.max_delay, args.output_prefix)
