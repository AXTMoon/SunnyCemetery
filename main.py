import src.Crawler
import argparse
import os

def mainParser():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Crawl websites and extract unique domains Version 0.6 (≖︿≖✿)")
    parser.add_argument('url', type=str, nargs='?', help="The starting URL to crawl (optional if using --url_file)")
    parser.add_argument('--url_file', type=str, help="Path to a file containing multiple URLs (one per line)")
    parser.add_argument('--depth', type=int, default=2, help="Maximum depth to crawl (default: 2)")
    parser.add_argument('--delay', type=float, default=0.1, help="Delay between requests in seconds (default: 0.1)")
    parser.add_argument('--max_workers', type=int, default=5, help="Number of concurrent workers for crawling (default: 5)")
    parser.add_argument('--proxy', type=str, help="Path to the proxy file (e.g., proxies.txt)")
    parser.add_argument('--proxy_rotation_interval', type=int, default=10, help="Number of requests before rotating the proxy (default: 10)")
    parser.add_argument('--timeout_limit', type=int, default=1, help="Maximum number of timeouts before skipping a URL (default: 1)")
    parser.add_argument('--output_nuclei', action='store_true', help="Save output in Nuclei format (one domain per line)")
    parser.add_argument('--output_openvas', action='store_true', help="Save output in OpenVAS format (domains separated by commas)")
    parser.add_argument('--output_tree', action='store_true', help="Save the domain tree of the scan")

    # Parse the arguments
    args = parser.parse_args()

    if args.url_file:
        if not os.path.isfile(args.url_file):
            print(f"Error: The file '{args.url_file}' does not exist.")
            return

        # Read URLs from file
        with open(args.url_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]

        if not urls:
            print("Error: The URL file is empty.")
            return

        # Crawl each URL
        for url in urls:
            print(f"\nStarting crawl for: {url}")
            src.Crawler.start_crawling(
                start_url=url,
                max_depth=args.depth,
                delay=args.delay,
                max_workers=args.max_workers,
                proxy_file=args.proxy,
                proxy_rotation_interval=args.proxy_rotation_interval,
                timeout_limit=args.timeout_limit,
                output_nuclei=args.output_nuclei,
                output_openvas=args.output_openvas,
                output_tree=args.output_tree
            )
    elif args.url:
        # Crawl a single URL
        src.Crawler.start_crawling(
            start_url=args.url,
            max_depth=args.depth,
            delay=args.delay,
            max_workers=args.max_workers,
            proxy_file=args.proxy,
            proxy_rotation_interval=args.proxy_rotation_interval,
            timeout_limit=args.timeout_limit,
            output_nuclei=args.output_nuclei,
            output_openvas=args.output_openvas,
            output_tree=args.output_tree
        )
    else:
        print("Error: You must provide either a URL or a URL file. Try using -h for more info.")

if __name__ == "__main__":
    mainParser()
