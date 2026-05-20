# app.py

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="News Feed",
    page_icon="📰",
    layout="wide"
)

NEWS_API_URL = "https://newsapi.org/v2/top-headlines"


@st.cache_data(ttl=600)
def fetch_news(api_key, country="us", category=None, query=None, page_size=20):
    params = {
        "apiKey": api_key,
        "pageSize": page_size,
    }

    if query:
        params["q"] = query
    else:
        params["country"] = country

    if category and category != "All":
        params["category"] = category.lower()

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def format_date(date_string):
    if not date_string:
        return "Date unavailable"

    try:
        dt = datetime.fromisoformat(date_string.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return date_string


def display_article(article):
    source = article.get("source", {}).get("name", "Unknown source")
    title = article.get("title") or "Untitled"
    description = article.get("description") or "No description available."
    url = article.get("url")
    image_url = article.get("urlToImage")
    published_at = format_date(article.get("publishedAt"))
    author = article.get("author")

    with st.container(border=True):
        col1, col2 = st.columns([1, 3])

        with col1:
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.write("📰")

        with col2:
            st.subheader(title)
            st.caption(f"{source} • {published_at}")

            if author:
                st.caption(f"By {author}")

            st.write(description)

            if url:
                st.link_button("Read full article", url)


def main():
    st.title("📰 Live News Feed")

    api_key = "a3f417b116fa4104b3c547e8ee9d32e1"

    if not api_key:
        st.error("NEWS_API_KEY is missing. Add it to `.streamlit/secrets.toml`.")
        st.stop()

    with st.sidebar:
        st.header("Filters")

        country = st.selectbox(
            "Country",
            ["us", "in", "gb", "au", "ca"],
            index=0
        )

        category = st.selectbox(
            "Category",
            [
                "All",
                "Business",
                "Entertainment",
                "General",
                "Health",
                "Science",
                "Sports",
                "Technology"
            ]
        )

        query = st.text_input("Search query", placeholder="e.g. AI, economy, sports")

        page_size = st.slider("Number of articles", 5, 50, 20)

        fetch_button = st.button("Fetch News")

    try:
        data = fetch_news(
            api_key=api_key,
            country=country,
            category=category,
            query=query,
            page_size=page_size
        )

        if data.get("status") != "ok":
            st.error("Could not fetch news successfully.")
            st.json(data)
            return

        articles = data.get("articles", [])

        st.caption(f"Showing {len(articles)} articles")

        if not articles:
            st.warning("No articles found.")
            return

        for article in articles:
            display_article(article)

    except requests.exceptions.RequestException as e:
        st.error("Network or API error while fetching news.")
        st.exception(e)

    except Exception as e:
        st.error("Something went wrong.")
        st.exception(e)


if __name__ == "__main__":
    main()