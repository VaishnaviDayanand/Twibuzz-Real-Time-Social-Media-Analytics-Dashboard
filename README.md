# Twibuzz-Real-Time-Social-Media-Analytics-Dashboard

This project presents a real-time analytics pipeline built to fetch, process, and visualize tweets from X (formerly Twitter) using Python. It enables users to gain meaningful insights into tweet sentiment, hashtag trends, user mentions, and tweet activity in a clean and interactive Streamlit web app.


🚀 Features
✅ Real-time Tweet Feed – Displays tweets in a feed-like format.
✅ Sentiment Analysis – Classifies tweets as Positive, Negative, or Neutral using VADER.
✅ Trending Hashtags – Identifies most used hashtags.
✅ Most Mentioned Users – Highlights frequently tagged usernames.
✅ Tweet Activity Over Time – Visualizes when tweets were posted with fine time granularity.
✅ Word Cloud – Displays most common words across tweets.
✅ Interactive Dashboard – Easy navigation across multiple views (Home, Tweets Window, Dashboard, About).

🛠️ Tech Stack
Python
Streamlit – Dashboard development
NLTK (VADER) – Sentiment analysis
Pandas – Data processing
Matplotlib / Seaborn / WordCloud – Visualizations


📉 Visualizations Included
Sentiment Distribution
Top Hashtags
Most Mentioned Users
Tweet Activity Timeline (millisecond precision)
Word Cloud
Real-time Tweet Feed



📌 Limitations
X API limits to 100 tweets per request
Real-time tweets fetched before likes/comments accumulate, so engagement metrics are minimal