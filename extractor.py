import concurrent.futures
import requests
from bs4 import BeautifulSoup

input_filename = "extracted_hrefs.txt"
output_filename = "extracted_data.txt"

def read_urls(filename):
    """Read URLs from a file and filter those starting with 'https://bunkrrr.org'."""
    with open(filename, "r") as file:
        lines = file.readlines()

    urls = [line.strip() for line in lines if line.startswith("https://bunkrrr.org")]

    return urls

def fetch(url):
    """Fetch content from a URL with a timeout of 10 seconds."""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
        print(f"Fetched successfully: {url}")
        return response.text, url
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, url

def extract_data_from_url(url):
    """Extract specific data from a given URL."""
    content, url = fetch(url)
    if content:
        try:
            print(f"Extracting data from: {url}")
            soup = BeautifulSoup(content, "html.parser")
            span = soup.find("span", class_="text-[16px] break-normal", style="color: #272727;background: #ffd369;font-weight: bold;margin-bottom: 7px;ext-align: left !important;")
            if span:
                data = span.text.strip()
                print(f"Data extracted from {url}: {data}")
                return url, data
        except Exception as e:
            print(f"Error parsing content from {url}: {e}")
    return url, None

def save_extracted_data(url, data, filename):
    """Save extracted data to a file."""
    with open(filename, "a") as file:
        if data:
            file.write(f"{url}: {data}\n")
            print(f"Written to file: {url}: {data}")

def process_url(url):
    """Fetch and extract data from a URL, then save to file."""
    url, data = extract_data_from_url(url)
    save_extracted_data(url, data, output_filename)
    return url, data

def main():
    urls = read_urls(input_filename)
    print(f"Total URLs to process: {len(urls)}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result[1] is not None:
                    print(f"Processed: {result[0]}")
            except Exception as exc:
                print(f"URL processing generated an exception: {exc}")

    print("Data extraction complete. Check the output file for results.")

if __name__ == "__main__":
    main()
