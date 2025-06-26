# News API Client

A Python client for the [NewsAPI.org](https://newsapi.org/) service to fetch news articles from various sources with a Streamlit web interface.

## NewsAPI.org Pricing

NewsAPI.org offers both free and paid plans:

### Free Plan (Developer)
- 100 requests per day
- Limited to headlines from the last month
- No commercial use allowed
- Basic search functionality
- Perfect for personal projects, learning, and testing

### Paid Plans
- Start from $449/month (Business plan)
- Higher request limits
- Full article search with no time restrictions
- Commercial use allowed
- More features and fewer restrictions

You can start with the free plan to test the API and this client. Sign up at [NewsAPI.org](https://newsapi.org/) to get your API key.

## Features

- Fetch top headlines by country, category, or source
- Search for news articles using keywords
- Get news from specific sources or domains
- Display news articles in a readable format

## Requirements

- Python 3.6+
- NewsAPI.org API key (get one for free at [https://newsapi.org/](https://newsapi.org/))

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API key:
   - Open the `.env` file and replace `your_api_key_here` with your actual NewsAPI key
   - Alternatively, you can set it as an environment variable: `NEWSAPI_KEY=your_api_key_here`

## Usage

### Streamlit Web App (Recommended)

Run the Streamlit web application for an interactive news browsing experience:

```bash
streamlit run app.py
```

This will launch a web interface in your browser where you can:
- Search for top headlines by country and category
- Perform comprehensive searches with keywords
- Filter by sources, domains, language, and date
- View article images, descriptions, and links
- Use quick search buttons for popular categories

### Command Line Examples

Alternatively, you can run the example scripts from the command line:

```bash
# Run predefined examples
python news.py

# Run interactive command-line search tool
python custom_search.py
```

## Using the NewsAPIClient in Your Own Code

```python
from news import NewsAPIClient

# Initialize the client with your API key
client = NewsAPIClient("your_api_key_here")
# Or let it use the key from environment variables
# client = NewsAPIClient()

# Get top headlines
headlines = client.get_top_headlines(country="in", category="business")
articles = headlines.get('articles', [])

# Search for specific news
results = client.get_everything(q="climate change", sort_by="relevancy")
articles = results.get('articles', [])

# Get news from specific sources
bbc_news = client.get_everything(sources="bbc-news")
articles = bbc_news.get('articles', [])
```

## API Methods

### `get_top_headlines`

Get breaking news headlines from various sources.

Parameters:
- `country` (str, optional): The 2-letter ISO 3166-1 code of the country. Default is "us".
- `category` (str, optional): The category to get headlines for. Options: business, entertainment, general, health, science, sports, technology.
- `sources` (str, optional): A comma-separated string of identifiers for the news sources or blogs.
- `q` (str, optional): Keywords or phrases to search for in the article title and body.
- `page_size` (int, optional): The number of results to return per page. Default is 10, maximum is 100.
- `page` (int, optional): The page number to return. Default is 1.

### `get_everything`

Search through millions of articles from over 80,000 large and small news sources and blogs.

Parameters:
- `q` (str, optional): Keywords or phrases to search for in the article title and body.
- `sources` (str, optional): A comma-separated string of identifiers for the news sources or blogs.
- `domains` (str, optional): A comma-separated string of domains to restrict the search to.
- `from_date` (str, optional): A date in ISO 8601 format (e.g., "2023-12-01").
- `to_date` (str, optional): A date in ISO 8601 format (e.g., "2023-12-31").
- `language` (str, optional): The 2-letter ISO-639-1 code of the language. Default is "en".
- `sort_by` (str, optional): The order to sort articles in. Options: relevancy, popularity, publishedAt.
- `page_size` (int, optional): The number of results to return per page. Default is 10, maximum is 100.
- `page` (int, optional): The page number to return. Default is 1.

### `get_sources`

Get all the news sources available in the API.

Parameters:
- `category` (str, optional): The category to filter sources by. Options: business, entertainment, general, health, science, sports, technology.
- `language` (str, optional): The 2-letter ISO-639-1 code of the language. Default is "en".
- `country` (str, optional): The 2-letter ISO 3166-1 code of the country.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
