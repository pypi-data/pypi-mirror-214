# bio2csv

`bio2csv` is a Python package that allows you to easily scrape biology research papers from BioRxiv. It retrieves details such as the title, authors, and link of each paper, and it can also fetch the abstract and the full text if specified.

## Installation

You can install the `bio2csv` package with pip:

```bash
pip install bio2csv
```

## Usage

Here's a simple usage example:

```python
from bio2csv import scrape_biorxiv

# Scrape the first 10 pages of genetics collection and get the abstract and full text of each paper
df = scrape_biorxiv(pages=10, get_abstract=True, get_full_text=True)

# Print the resulting DataFrame
print(df)
```

You can also use the `fetch_paper_details` function to fetch the abstract and full text of a single paper:

```python
from bio2csv import fetch_paper_details
import requests

# Initialize a session
session = requests.Session()

# URL of the paper
paper_url = "https://www.biorxiv.org/content/10.1101/2023.06.16.448484v1"

# Fetch details
abstract, full_text = fetch_paper_details(paper_url, session)

# Print details
print(f"Abstract: {abstract}")
print(f"Full Text: {full_text}")
```

Please note that the `fetch_paper_details` function needs an active `requests.Session()` to work.

## Contributing

Contributions to `bio2csv` are welcome! If you have a feature request, bug report, or proposal, please open an issue on this repository. If you wish to contribute code, please fork the repository, make your changes, and submit a pull request.

## License

`bio2csv` is released under the MIT License. For more details, see the `LICENSE` file in this repository.