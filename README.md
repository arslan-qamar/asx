# ASX Listings Web Crawler and Notifier

This project is a web crawler that scrapes ASX-listed company data from the [Market Index](https://www.marketindex.com.au/asx-listed-companies) website. It periodically fetches new listings and stores them in a database. If new listings are found, a notification is sent to a Telegram bot chat.

## Features

- Scrapes ASX-listed companies from the Market Index website.
- Stores fetched data in a MongoDB database.
- Periodically checks for newly listed companies.
- Sends notifications via a Telegram bot when a new listing is detected.
- Automated execution using GitHub Actions.

## Technologies Used

- **Python** (Primary programming language)
- **Requests** (For HTTP requests)
- **BeautifulSoup** (For HTML parsing and data extraction)
- **MongoDB** (For storing ASX listings data)
- **Python-Telegram-Bot** (For sending notifications via Telegram)
- **GitHub Actions** (For automating data fetching and notifications)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/asx-listings-bot.git
   cd asx-listings-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   export bot_token="your_telegram_bot_token"
   export bot_chatid="your_telegram_chat_id"
   export asx_db="your_mongodb_connection_string"
   ```
4. Run the fetcher script:
   ```bash
   python start_fetcher.py
   ```
5. Run the notifier script:
   ```bash
   python start_notifier.py
   ```

## Project Structure
```
.
├── Ingestion/
│   ├── start_fetcher.py  # Fetches ASX listings and updates DB
│   ├── requirements.txt  # Dependencies for ingestion
├── Notifier/
│   ├── start_notifier.py  # Checks for new listings and notifies Telegram
│   ├── requirements.txt  # Dependencies for notifier
├── storage/
│   ├── storagemanager.py  # Handles MongoDB interactions
├── .github/workflows/
│   ├── fetcher.yml  # GitHub Action for fetching listings
│   ├── notifier.yml  # GitHub Action for notifying Telegram
├── README.md  # Project documentation
└── requirements.txt
```

## GitHub Actions Workflow

### Fetcher Pipeline
- Runs every 4 hours to fetch ASX listings.
- Updates the MongoDB database.

```yaml
on:
  schedule:
    - cron: "0 */4 * * *"
```

### Notifier Pipeline
- Runs every 5 hours to check for new listings.
- Sends notifications to the Telegram bot if a new listing is found.

```yaml
on:
  schedule:
    - cron: "0 */5 * * *"
```

## License
This project is licensed under the MIT License.

## Author
Arslan Qamar - [Asx Listings Web Crawler and Notifier](https://github.com/arslan-qamar/Asx)

---

Feel free to modify and expand the project as needed!


