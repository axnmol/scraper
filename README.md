# Comparative Analysis for Booking.com and Expedia

This project scrapes hotel data from **Booking.com** and **Expedia** for 5-star hotels in New York City. The data includes hotel names, ratings, prices, reviews, and amenities. The project uses Selenium WebDriver to automate browser interactions and stores the scraped data in JSON format.

## Project Structure
```
.
├── booking.py
├── booking_2024-10-01_2024-10-31.json
├── common.py
├── driver
│   ├── LICENSE.chromedriver
│   ├── THIRD_PARTY_NOTICES.chromedriver
│   └── chromedriver
├── expedia.py
├── expedia_2024-10-01_2024-10-31.json
├── scrap.ipynb
└── scripts.py
```

### Key Files

- **`booking.py`**: Scrapes hotel data from Booking.com.
- **`expedia.py`**: Scrapes hotel data from Expedia.
- **`common.py`**: Contains utility functions for finding elements in the DOM.
- **`scripts.py`**: JavaScript snippets for scrolling through the webpage.
- **`scrap.ipynb`**: Jupyter notebook that orchestrates the scraping process and saves data to JSON files and performs Comparative Analysis.
- **`driver/`**: Directory containing the Chrome WebDriver required for Selenium.

## Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
