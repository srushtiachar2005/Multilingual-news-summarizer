# --- news_utils.py ---
import streamlit as st
from datetime import datetime
import re
from html import unescape
import requests
from bs4 import BeautifulSoup
import os



def translate_text(text, target_lang):
   
    return text

def display_articles(articles, target_lang=None, image_width=300):
    if not articles:
        st.warning("No articles to display.")
        return

    for article in articles:
        st.markdown("---")
        title = article.get("title", "No Title")
        description = article.get("description") or article.get("content") or "No description available."

        st.subheader(title)

        if article.get("urlToImage"):
            st.image(article["urlToImage"], width=image_width)

        source = article.get("source", {}).get("name", "Unknown Source")
        published_at = article.get("publishedAt", "")
        if published_at:
            try:
                dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
                published_at = dt.strftime("%b %d, %Y at %I:%M %p")
            except:
                pass
        st.caption(f"📳 {source} | 🕒 {published_at}")

        st.write(description)

        url = article.get("url", "#")
        st.markdown(f"[🔗 Read full article]({url})", unsafe_allow_html=True)

def extract_text_and_link(raw_html):
    match = re.search(r'<a href="([^"]+)"[^>]*>(.*?)</a>', raw_html)
    link = match.group(1) if match else ""
    title = unescape(match.group(2)) if match else unescape(raw_html)
    publisher_match = re.search(r'<font[^>]*>(.*?)</font>', raw_html)
    publisher = unescape(publisher_match.group(1)) if publisher_match else "Unknown Publisher"
    return title.strip(), link.strip(), publisher.strip()

def extract_image(entry):
    if "media_content" in entry and entry.media_content:
        return entry.media_content[0].get("url")
    if "media_thumbnail" in entry and entry.media_thumbnail:
        return entry.media_thumbnail[0].get("url")
    img_match = re.search(r'<img[^>]+src="([^">]+)"', entry.get("summary", ""))
    return img_match.group(1) if img_match else None

def fetch_og_image(article_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(article_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
    except Exception:
        pass
    return None

def display_rss_feed(rss_url, filter_date=None):
    import feedparser
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        st.warning("No RSS feed articles available.")
        return

    matched_entries = []
    for entry in feed.entries:
        try:
            published = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
            if filter_date and published.date() != filter_date:
                continue
            matched_entries.append((entry, published))
        except Exception:
            continue

    if not matched_entries:
        st.warning(f"No RSS articles published on {filter_date.strftime('%Y-%m-%d')}.")
        return

    st.success(f"Fetched {len(matched_entries)} RSS articles for {filter_date.strftime('%Y-%m-%d')}.")

    for entry, published in matched_entries:
        st.markdown("---")
        title, link, publisher = extract_text_and_link(entry.title)
        image_url = extract_image(entry)
        if not image_url:
            image_url = fetch_og_image(link)
        if image_url:
            st.image(image_url, width=400)
        st.subheader(title)
        st.caption(f"📳 {publisher} | 🕒 {published.strftime('%b %d, %Y at %I:%M %p')}")
        summary = entry.get("summary") or "No summary available."
        st.write(summary)
        st.markdown(f"[🔗 Read full article]({link})", unsafe_allow_html=True)
