# ACM Digital Library Scraper

This project is a hobby initiative designed to practice web scraping techniques. The scraper targets the ACM Digital Library, utilizing Selenium and BeautifulSoup to perform keyword-based searches. It extracts key details from academic articles, including titles, authors, publication years, and DOI links.

---

## Installation Guide

1. **Clone the repository**  
```bash
   git clone https://github.com/ruokokoski/acm-webscraper.git
   cd acm-webscraper
```

2. **Install dependencies**

  Ensure you have Poetry installed. Then run:
```bash
  poetry install
```

3. **Set up the WebDriver**

  Download the compatible WebDriver for your browser (e.g., ChromeDriver) and ensure it's added to your system's PATH.

---

## Usage

Run the scraper with the following command:
```bash
  python3 acm_scraper.py "search words"
```

Replace "search words" with your desired keywords. The scraper will fetch and display academic article details based on your query.




