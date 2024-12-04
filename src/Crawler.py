"""
Crawler for SunnyCemetery with Proxy Rotation
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import time
import concurrent.futures
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import itertools

# Function to load proxies from a file
def load_proxies(file_path):
    try:
        with open(file_path, "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            raise ValueError("Proxy file is empty.")
        return proxies
    except Exception as e:
        print(f"Error loading proxy file: {e}")
        return []

# Function to create a requests session with retries and a rotating proxy
def create_session(proxy=None):
    session = requests.Session()

    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('http://', HTTPAdapter(max_retries=retries))
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    if proxy:
        session.proxies = {"http": proxy, "https": proxy}
    
    return session

# Function to extract all links (URLs) from a webpage
def extract_links(url, session, timeout_limit):
    timeout_retries = 0
    while timeout_retries < timeout_limit:
        try:
            headers = {
                "Accept": "text/html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            unique_urls = set()

            for link in links:
                href = link.get('href')
                if re.match(r'^https?://', href):
                    unique_urls.add(href)
                elif href.startswith('/'):
                    base_url = url.rstrip('/')
                    unique_urls.add(urljoin(url, href))

            return unique_urls

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            timeout_retries += 1
            print(f"Timeout occurred for {url}. Retry {timeout_retries}/{timeout_limit}.")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred while fetching {url}: {e}")
            break

    print(f"Exceeded timeout limit for {url}. Skipping.")
    return set()

# Function to rotate proxies during crawling
def start_crawling(start_url, max_depth=2, delay=0.1, max_workers=5, proxy_file=None, proxy_rotation_interval=0, timeout_limit=1):
    visited_urls = set()
    proxies = itertools.cycle(load_proxies(proxy_file)) if proxy_file else None
    session = create_session(next(proxies) if proxies else None)

    # Counter to track when to rotate the proxy
    request_counter = 0

    # Tree structure to track domain hierarchy
    domain_tree = {}

    def get_rotated_session():
        nonlocal request_counter
        request_counter += 1
        if proxies and request_counter % proxy_rotation_interval == 0:
            print("Rotating proxy...")
            return create_session(next(proxies))
        return session

    def crawl_recursive(url, depth, parent_node):
        if depth > max_depth or url in visited_urls:
            return
        visited_urls.add(url)
        print(f"Crawling depth {depth}: Extracting links from {url}...")

        current_session = get_rotated_session()
        child_urls = extract_links(url, current_session, timeout_limit)
        unique_domains = {urlparse(u).netloc for u in child_urls}

        # Add the current domain's children to the tree
        current_domain = urlparse(url).netloc
        if current_domain not in parent_node:
            parent_node[current_domain] = {}
        current_node = parent_node[current_domain]

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(crawl_recursive, u, depth + 1, current_node): u
                for u in child_urls if u not in visited_urls
            }
            for future in concurrent.futures.as_completed(futures):
                pass

    crawl_recursive(start_url, depth=1, parent_node=domain_tree)

    def write_tree_to_file(tree, file, indent=0):
        for domain, children in tree.items():
            file.write("  " * indent + domain + "\n")
            write_tree_to_file(children, file, indent + 1)

    domain = urlparse(start_url).netloc
    domain_name = domain.replace('www.', '').replace('.', '_')
    output_file = f"out/{domain_name}_domain_tree.txt"

    with open(output_file, "w") as f:
        write_tree_to_file(domain_tree, f)

    print(f"\nDomain tree has been written to {output_file}")