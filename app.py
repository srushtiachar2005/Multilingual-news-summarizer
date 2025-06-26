# --- app.py ---
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from news_client import NewsAPIClient
from news_utils import display_articles, display_rss_feed

# Load API keys from .env
load_dotenv()


st.set_page_config(page_title="📰 Dहooతha", layout="wide")


st.title("📰 Dहooతha: Daily News Summarizer")


client = NewsAPIClient()


st.sidebar.header("📋 Filters")


LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}
language_name = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
language_code = LANGUAGES[language_name]


NEWS_SOURCES = {
    "All Sources": None,
    "BBC News": "bbc-news",
    "CNN": "cnn",
    "Reuters": "reuters",
    "The Verge": "the-verge",
    "TechCrunch": "techcrunch",
    "Google News (IN)": "google-news-in",
    "The Times of India": "the-times-of-india",
}
source_name = st.sidebar.selectbox("News Source", list(NEWS_SOURCES.keys()), index=0)
source_code = NEWS_SOURCES[source_name]


query = st.sidebar.text_input("Search Keyword", value="Technology")
selected_date = st.sidebar.date_input("Select Date", datetime.now().date())


if st.sidebar.button("Fetch News"):
    try:
        date_str = selected_date.strftime("%Y-%m-%d")

        if source_code:
            response = client.get_everything(
                q=query,
                sources=source_code,
                from_param=date_str,
                to=date_str,
                language="en",
                sort_by="publishedAt",
                page_size=100
            )
        else:
            response = client.get_everything(
                q=query,
                from_param=date_str,
                to=date_str,
                language="en",
                sort_by="publishedAt",
                page_size=100
            )

        raw_articles = response.get("articles", [])
        articles = []
        for article in raw_articles:
            published_at = article.get("publishedAt", "")
            if published_at:
                try:
                    dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                    if dt.date() == selected_date:
                        articles.append(article)
                except:
                    continue

        if articles:
            st.success(f"✅ Found {len(articles)} articles for {selected_date.strftime('%Y-%m-%d')}.")
            display_articles(articles, target_lang=language_code)
        else:
           
            rss_shown = False
            if source_code == "bbc-news" or source_code is None:
                topic_rss_map = {
                    "technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
                    "tech": "https://feeds.bbci.co.uk/news/technology/rss.xml",
                    "sports": "https://feeds.bbci.co.uk/sport/rss.xml",
                    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
                    "world": "https://feeds.bbci.co.uk/news/world/rss.xml"
                }
                topic = query.lower().strip()
                rss_url = topic_rss_map.get(topic, "https://feeds.bbci.co.uk/news/rss.xml")
                display_rss_feed(rss_url, filter_date=selected_date)
                rss_shown = True
            
            if not rss_shown:
                st.warning(f"🚫 No articles found for '{query}' on {selected_date.strftime('%Y-%m-%d')}.")

    except Exception as e:
        st.error(f"❌ Error fetching news: {e}")
else:
    st.markdown("👈 Use the sidebar to choose filters and click **Fetch News**.")
