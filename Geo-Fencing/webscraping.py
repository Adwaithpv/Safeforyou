import feedparser  # Library to parse RSS feeds
import pandas as pd  # Library for data manipulation and saving to CSV

# Define the RSS feed URL for news related to molestation, rape, or harassment in Chennai
rss_url = "https://news.google.com/rss/search?q=molestation+OR+rape+OR+harassment+in+Chennai"

# Parse the RSS feed using feedparser
feed = feedparser.parse(rss_url)

# Create an empty list to store article details
articles = []

# Loop through each news entry in the RSS feed
for entry in feed.entries:
    title = entry.title        # Get the title of the news article
    link = entry.link          # Get the URL link to the article
    published = entry.published  # Get the published date of the article

    # Append the article details as a dictionary to the articles list
    articles.append({
        "title": title,
        "link": link,
        "published": published
    })

# Convert the list of articles into a pandas DataFrame
df = pd.DataFrame(articles)

# Save the DataFrame to a CSV file
df.to_csv("women_safety_news_chennai.csv", index=False)

# Print a success message showing the number of articles scraped
print(f"Scraped {len(df)} articles. Saved to 'women_safety_news_chennai.csv'.")
