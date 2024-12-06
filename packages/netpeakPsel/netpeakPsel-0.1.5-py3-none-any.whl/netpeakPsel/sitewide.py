import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import csv
import re
from tqdm import tqdm
import lxml.etree as ET
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class RequestHandler:
    def __init__(self, delay=1):
        self.delay = delay

    def make_request(self, url):
        """Performs HTTP request with delay."""
        try:
            time.sleep(self.delay)  # Delay before request
            response = requests.get(url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error while requesting {url}: {e}")
            return None

class CacheManager:
    def __init__(self, cache_file='cache.txt'):
        self.cache_file = cache_file
        self.cache = self.load_cache()

    def load_cache(self):
        """Loads cache from a text file."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return set(line.strip() for line in f)
        return set()

    def save_cache(self):
        """Saves updated cache to a text file."""
        with open(self.cache_file, 'w') as f:
            for url in self.cache:
                f.write(f"{url}\n")

    def check_cache(self, url):
        """Checks if a URL has already been processed."""
        return url in self.cache

    def update_cache(self, url):
        """Adds a new URL to the cache."""
        self.cache.add(url)
        self.save_cache()

class Crawler:
    def __init__(self, request_handler, cache_manager):
        self.request_handler = request_handler
        self.cache_manager = cache_manager
        self.sitewide_elements = ['header', 'footer', 'nav', 'aside']
        self.blog_pattern = re.compile(r'/blog/?$', re.IGNORECASE) #Regular expression to match blog URLs

    def ensure_scheme(self, url):
        """Adds https:// to the URL if the scheme is missing."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return f"https://{url}"
        return url

    def normalize_domain(self, url):
        """Normalizes the domain by removing 'www.' if present."""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    def is_external_link(self, link, base_url):
        """Checks if the link is external compared to the base URL."""
        domain_link = self.normalize_domain(link)
        domain_base = self.normalize_domain(base_url)
        return domain_link != domain_base

    def get_xpath(self, element):
        """Returns the XPath of an element."""
        return element.getroottree().getpath(element)

    def find_blog_page(self, url):
        """Finds the blog page by looking for a URL containing 'blog'."""
        response = self.request_handler.make_request(url)
        if response is None:
            return None

        soup = BeautifulSoup(response.text, 'lxml')

        # Look for the first link with 'blog' in the URL
        blog_link = None
        for link in soup.find_all('a', href=True):
            if re.search(r'/blog', link['href']):
                blog_link = urljoin(url, link['href'])
                break

        return blog_link

    def get_sitewide_external_links(self, url, use_cache=True):
        """Extracts external links from sitewide elements (header, footer, nav, aside)."""
        if use_cache and self.cache_manager.check_cache(url):
            print(f"{Fore.WHITE}Page {Fore.YELLOW}{url} {Fore.WHITE}is already cached, skipping.")
            return set()

        response = self.request_handler.make_request(url)
        if response is None:
            return set()

        soup = BeautifulSoup(response.text, 'lxml')
        dom = ET.HTML(str(soup))

        external_links = set()
        for element in self.sitewide_elements:
            for tag in soup.find_all(element):
                for link in tag.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    if self.is_external_link(full_url, url):
                        lxml_elements = dom.xpath(f"//a[@href='{href}']")
                        if lxml_elements:
                            link_xpath = self.get_xpath(lxml_elements[0])
                            external_links.add((full_url, link_xpath, url))

        if use_cache:
            self.cache_manager.update_cache(url)
            self.cache_manager.save_cache()

        return external_links


    def parse_url(self, url):
        """Parses a single URL, finds external links on both the main page and blog page."""
        url = self.ensure_scheme(url)
        domain = self.normalize_domain(url)

        output_file = f"{domain}_sitewide_links.csv"
        print(f"{Fore.WHITE}Parsing {Fore.YELLOW}{url} {Fore.WHITE}and saving results to {output_file}...")

        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])

            # Parse main page external sitewide links (no cache for parse_url)
            external_links = self.get_sitewide_external_links(url, use_cache=False)
            for link, xpath, page_url in external_links:
                csv_writer.writerow([url, link, xpath, page_url])

            # Check if there's a blog page, and parse it
            blog_page = self.find_blog_page(url)
            if blog_page:
                print(f"{Fore.WHITE}Found blog page at {Fore.YELLOW}{blog_page}")
                blog_external_links = self.get_sitewide_external_links(blog_page, use_cache=False)
                for link, xpath, page_url in blog_external_links:
                    csv_writer.writerow([blog_page, link, xpath, page_url])

        print(f"{Fore.GREEN}Results for {Fore.YELLOW}{url} {Fore.GREEN}saved to {output_file}")

    def parse_list_domain(self, domain_file, output):
        """Parses domains from a file, processes both the main page and the blog page, and saves the result to a single CSV file."""
        with open(domain_file, 'r') as f:
            domains = [line.strip() for line in f]

        # Determine if there is at least one domain that has not yet been processed and is not in the cache
        new_domains_to_process = [
            domain for domain in domains if not self.cache_manager.check_cache(self.ensure_scheme(domain))
        ]

        # If there are no new domains, print the message and terminate the function
        if not new_domains_to_process:
            print(f"{Fore.GREEN}All domains are already cached. No new domains to process.")
            return

        # Check if the file with the results exists
        file_exists = os.path.isfile(output)

        # Open the file for writing, if the file exists, open it in add mode, otherwise in write mode
        with open(output, 'a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # If the file did not exist, record the headers
            if not file_exists:
                writer.writerow(['Domain', 'External Link', 'XPath', 'Page URL'])

            # We process only new domains
            for domain in tqdm(new_domains_to_process, desc="Scanning domains", bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.YELLOW, Fore.RESET)):
                domain = self.ensure_scheme(domain)

                # Collect external links from the home page
                external_links = self.get_sitewide_external_links(domain)
                for link, xpath, page_url in external_links:
                    writer.writerow([domain, link, xpath, page_url])

                # Looking for a blog page and collecting external links if possible
                blog_page = self.find_blog_page(domain)
                if blog_page:
                    blog_external_links = self.get_sitewide_external_links(blog_page)
                    for link, xpath, page_url in blog_external_links:
                        writer.writerow([blog_page, link, xpath, page_url])

        print(f"{Fore.GREEN}New results saved to {output}")


