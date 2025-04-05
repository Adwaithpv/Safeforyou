import feedparser
import pandas as pd

rss_url = "https://news.google.com/rss/search?q=molestation+OR+rape+OR+harassment+in+Chennai"

feed = feedparser.parse(rss_url)

articles = []
for entry in feed.entries:
    title = entry.title
    link = entry.link
    published = entry.published
    articles.append({"title": title, "link": link, "published": published})

df = pd.DataFrame(articles)
df.to_csv("women_safety_news_chennai.csv", index=False)

print(f"Scraped {len(df)} articles. Saved to 'women_safety_news_chennai.csv'.")
