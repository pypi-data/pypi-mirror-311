import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
import csv


class ContentParser:
    def __init__(self, start_url, search_word, output_file="results.csv"):
        self.start_url = start_url
        self.search_word = search_word.lower()
        self.output_file = output_file
        self.visited_urls = set()
        self.results = []

    def write_to_csv(self):
        """Writes the results to a CSV file."""
        with open(self.output_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Type", "Tag/Attribute", "Content"])
            writer.writerows(self.results)

    def search_word_in_html(self, url):
        """Searches for the word in the HTML content of the URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            for tag in soup.find_all(True):  # Iterate through all tags
                if tag.string and self.search_word in tag.string.lower():
                    self.results.append([url, "Tag", tag.name, tag.string.strip()])

                for attr, value in tag.attrs.items():  # Iterate through attributes
                    if isinstance(value, str) and self.search_word in value.lower():
                        self.results.append([url, "Attribute", f"{tag.name} {attr}", value.strip()])

            return soup

        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return None

    def crawl(self):
        """Crawls the website starting from the start URL."""
        urls_to_visit = [self.start_url]

        with tqdm(total=1, desc="Progress", unit="page") as pbar:
            while urls_to_visit:
                current_url = urls_to_visit.pop(0)

                if current_url in self.visited_urls:
                    continue

                self.visited_urls.add(current_url)

                soup = self.search_word_in_html(current_url)
                if not soup:
                    continue

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    next_url = urljoin(current_url, href)

                    if urlparse(next_url).netloc == urlparse(self.start_url).netloc:
                        if next_url not in self.visited_urls:
                            urls_to_visit.append(next_url)
                            pbar.total += 1
                            pbar.update(0)

                pbar.update(1)

        self.write_to_csv()
