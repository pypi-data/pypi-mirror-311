
# NetpeakPsel

**NetpeakPsel** is a tool for extracting external links from specific sections of web pages, such as `header`, `footer`, `nav`, and `aside`.

## Installation

You can install the package via `pip`:

```bash
pip install netpeakPsel
```

## How to Use?

### 1. Initializing Components

To start using the package, you need to initialize the main components:

```python
from netpeakPsel import *

# Initialize the request handler with a delay (default is 1 second)
request_handler = RequestHandler(delay=1)

# Initialize the cache manager with the cache file (default is 'cache.txt')
cache_manager = CacheManager(cache_file='cache.txt')

# Create the Crawler instance with the request handler and cache manager
crawler = Crawler(request_handler, cache_manager)

```

### 2. Parsing a Single URL

To extract external links from a single URL and save them in a CSV file:

```python
crawler.parse_url('https://example.com')
```

This will create a CSV file named `example.com_sitewide_links.csv` containing all the extracted external links.

### 3. Parsing a List of Domains from a File

To parse external links from multiple domains listed in a text file:

1. Create a file named `domains.txt` with each domain on a new line:
   ```
   example.com
   anotherdomain.com
   samplewebsite.org
   ```

2. Use the following command to parse all the domains and save the results in a single CSV file:

```python
crawler.parse_list_domain('domains.txt', 'sitewide_external_links.csv')
```

This will create a single CSV file (`sitewide_external_links.csv`) containing external links from all domains listed in `domains.txt`.

### 4. Full Website Content Parsing
To parse all content from a specific website:

```python
from netpeakPsel import ContentParser

parser = ContentParser("https://galinov.com/", "test.galinov.com", "results.csv")
parser.crawl()
```

## Features

- Extracts external links from the `header`, `footer`, `nav`, and `aside` sections of web pages.
- Caches processed URLs to avoid redundant parsing.
- Supports parsing multiple domains from a file.
- Saves results in CSV format for easy data analysis.

## Requirements

- Python 3.6 or later
- The following Python packages:
  - `requests`
  - `beautifulsoup4`
  - `lxml`
  - `tqdm`
  - `colorama`
  

These dependencies will be installed automatically when you install the package via `pip`.



## Contributing

If you'd like to contribute, feel free to fork the repository and submit a pull request. Please make sure to update tests as appropriate. [GitHub Repo](https://github.com/VsevolodKrasovskyi/netpeakPsel/)

