import argparse
from vulheader import check

def main():
    parser = argparse.ArgumentParser(description="HTTP Security Header Vulnerability Scanner")
    parser.add_argument("--url", required=True, help="Target URL (e.g., https://example.com)")
    parser.add_argument("-H", "--header", help="Specific header to check (optional)")

    args = parser.parse_args()
    url = args.url
    header = args.header

    if header:
        result = check(url, header)
        if result == "invalid_url":
            print(f"The URL {url} is not valid.")
        else:
            print(f"{header}: {'Present' if result == 'present' else 'Missing'}")
    else:
        result = check(url)
        if result == "invalid_url":
            print(f"The URL {url} is not valid.")
        else:
            for header, status in result.items():
                print(f"{header}: {'Present' if status == 'present' else 'Missing'}")

if __name__ == "__main__":
    main()
