# Hong Kong Law Society Firm Scraper

A Python script to ethically scrape publicly available law firm information from the Hong Kong Law Society website. This tool collects basic firm information while respecting privacy by excluding personal data.

## Features

- Scrapes basic firm information from the Hong Kong Law Society website
- Handles rate limiting with respectful delays between requests
- Implements error handling and timeout protection
- Saves data incrementally to prevent loss during long scraping sessions
- UTF-8 encoding support for proper handling of Chinese characters
- Excludes personal information (staff details) by design

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/hk-law-society-scraper.git
cd hk-law-society-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the scraper:
```bash
python hk_law_scraper.py
```

The script will:
- Scrape firm data from IDs 1 to 2000
- Save results incrementally to `law_firms_data.json`
- Display progress in the console

## Output Format

The script generates a JSON file with the following structure:

```json
[
  {
    "FirmId": 1,
    "Firm Name": "Example Law Firm",
    "Office Address": "123 Example Street, Hong Kong",
    ...
  },
  ...
]
```

## Ethical Considerations

This scraper is designed with the following ethical principles in mind:

- Respects the website's implicit rate limits with 1-second delays between requests
- Implements error handling to avoid server strain
- Excludes personal information (staff details) from collection
- Uses clear user-agent identification
- Saves data incrementally to avoid unnecessary repeat requests

## Legal Notice

This tool is intended for research and informational purposes only. Users should:

1. Review and comply with the Hong Kong Law Society's terms of service
2. Use the data in accordance with applicable laws and regulations
3. Implement appropriate delays between requests to avoid server strain

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This project is not affiliated with or endorsed by the Hong Kong Law Society. Users should ensure their use of this tool complies with the Hong Kong Law Society's terms of service and applicable laws.
