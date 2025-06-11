import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import base64

# Helper Function: Encode Image to Base64
def get_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set Background Images (Update paths for each section)
bg_images = {
    "Home": r"C:\Users\Admin\Desktop\Vaishu\RTSMADP\common.png",
    "Tweets Window": r"C:\Users\Admin\Desktop\Vaishu\RTSMADP\mainpage.png",
    "Analysis Dashboard": r"C:\Users\Admin\Desktop\Vaishu\RTSMADP\mainpage.png",
    "About": r"C:\Users\Admin\Desktop\Vaishu\RTSMADP\common.png",
}

# Custom CSS for Background (Dynamic based on the selected tab)
def set_bg(image_path):
    img_base64 = get_base64(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
        }}
        .content {{
            background: rgba(255, 255, 255, 0.8); 
            padding: 20px; 
            border-radius: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load processed dataset (ensure it's in the same directory)
@st.cache_data
def load_data():
    return pd.read_csv("processed_tweets.csv")

data = load_data()

# Set page configuration
#st.set_page_config(page_title="Social Media Analytics", page_icon="📊", layout="wide")

# Sidebar Navigation
selected_tab = st.sidebar.radio("Navigate", ["Home", "Tweets Window", "Analysis Dashboard", "About"], index=0)

# Set Background Image Based on Page
set_bg(bg_images[selected_tab])

# Home Page
if selected_tab == "Home":
    st.title("📊 TwiBuzz: Capturing the buzz across X (formerly Twitter)")

    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.header("Why Social Media Analytics Matters")

    st.write("""
    Social media analytics is a powerful tool that helps businesses, researchers, and marketers uncover hidden insights from online conversations. In today's fast-paced digital world, understanding social trends in real time is crucial for staying ahead.
    """)

    st.write("### 🔍 Why is Social Media Analytics Important?")

    st.markdown("""
    - **Real-Time Monitoring**: Capture live social media activity to stay informed about emerging trends and breaking news.  
    - **Sentiment Analysis**: Evaluate public perception by analyzing whether the sentiment is **positive**, **negative**, or **neutral**.  
    - **Trend Identification**: Identify popular hashtags, viral content, and trending topics to guide marketing strategies.  
    - **Crisis Detection**: Detect sudden shifts in sentiment to respond quickly to potential public relations issues.  
    - **Audience Understanding**: Gain insights into user demographics, behaviors, and preferences to better understand your audience.  
    - **Competitive Analysis**: Monitor competitor activity and audience reactions to maintain a competitive edge.  
    - **Strategic Decisions**: Use data-driven insights to refine marketing campaigns, product launches, and customer engagement strategies.  
    """)

    st.write("### 📈 What Can You Achieve with This Tool?")

    st.markdown("""
    Our **Real-Time Social Media Analytics** tool enables you to:

    - **Track** social media trends across time with millisecond precision.  
    - **Analyze** user engagement patterns and audience sentiment.  
    - **Visualize** data through intuitive dashboards and real-time feeds.  
    - **Enhance** decision-making by turning raw data into actionable insights.  
    - **Engage** with your audience by identifying what resonates with them.  

    This tool is designed to offer a **comprehensive view** of the social media landscape, empowering you to make **smarter, data-driven decisions**.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Tweets Window
elif selected_tab == "Tweets Window":
    import json

    # Load tweets from tweets.json
    @st.cache_data
    def load_tweets():
        with open("tweets.json", "r", encoding="utf-8") as file:
            return json.load(file)

    tweets = load_tweets()

    st.title("🗨️ Live Tweet Feed")

    # Display tweets like a social media feed
    for tweet in tweets:
        tweet_text = tweet.get("text", "No text available")
        tweet_id = tweet.get("id", None)
        created_at = tweet.get("created_at", "Unknown date")
        user = tweet.get("user", {}).get("name", "Unknown User")
        username = tweet.get("user", {}).get("screen_name", "unknown")

        tweet_url = f"https://twitter.com/{username}/status/{tweet_id}" if tweet_id else None

        st.markdown(f"""
            <div class="content">
                <strong>{user} (@{username})</strong><br>
                <span style="color: #555; font-size: 12px;">{created_at}</span><br><br>
                {tweet_text}<br><br>
                {"<a href='" + tweet_url + "' target='_blank'>🔗 View on Twitter</a>" if tweet_url else ""}
            </div>
        """, unsafe_allow_html=True)

# Analysis Dashboard
elif selected_tab == "Analysis Dashboard":
    st.title("📈 Analytics Dashboard")

    st.markdown("<div class='content'>", unsafe_allow_html=True)

    # Sentiment Distribution
    st.subheader("Sentiment Distribution")
    sentiment_counts = data['sentiment'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax, palette="Greens")
    st.pyplot(fig)

    # Top Hashtags
    st.subheader("Top Hashtags")
    hashtags = data['hashtags'].dropna()
    hashtags = hashtags[hashtags != '#[]'].str.split(',').sum()
    hashtag_counts = pd.Series(hashtags).value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=hashtag_counts.values, y=hashtag_counts.index, ax=ax, palette="Greens")
    st.pyplot(fig)

    # Most Mentioned Users
    st.subheader("Most Mentioned Users")
    mentions = data['entities'].dropna().str.extractall(r"'username': '([\w]+)'")[0]
    mentions = mentions[mentions != ""]
    mention_counts = mentions.value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=mention_counts.values, y=mention_counts.index, ax=ax, palette="Greens")
    st.pyplot(fig)

    # Tweet Activity Over Time
    st.subheader("Tweet Activity Over Time (Milliseconds Precision)")
    data['created_at'] = pd.to_datetime(data['created_at'])
    data['date'] = data['created_at'].dt.date
    data['time_detail'] = data['created_at'].dt.strftime("%H:%M:%S")
    time_series = data.groupby(['date', 'time_detail']).size().reset_index(name='count')
    plot_date = time_series['date'].iloc[0]
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='time_detail', y='count', data=time_series, ax=ax, color="#2E8B57")
    ax.set_xlabel(f"Time (HH:MM:SS) [Date: {plot_date}]")
    ax.set_ylabel("Number of Tweets")
    st.pyplot(fig)

    # Word Cloud
    st.subheader("Word Cloud")
    text = " ".join(data['text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

    st.markdown("</div>", unsafe_allow_html=True)

# About Page
elif selected_tab == "About":
    st.title("ℹ️ About Us")
    st.markdown("<div class='content'>", unsafe_allow_html=True)
    st.write("This app is developed by a team passionate about data analytics and social media insights.")
    st.markdown("""
    📌:
We are a group of three passionate engineers who designed this Real-Time Social Media Analytics Tool to track and analyze social media trends as they happen. Our goal is to provide valuable insights into public sentiment, engagement patterns, and trending topics.

Our Mission:
To empower businesses and researchers with real-time data from social media platforms, allowing them to:

- Monitor live trends and public sentiment.
- Gain actionable insights for decision-making.
- Enhance engagement tracking and performance analysis.
                
Meet the Team:
                
Mansi Manjunath Lokhandey: [LinkedIn Profile](https://www.linkedin.com/in/mansi-manjunath-lokhanday12?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)  
Priya G S: [LinkedIn Profile](https://www.linkedin.com/in/priya-g-s-510465289?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app)  
Vaishnavi D: [LinkedIn Profile](https://www.linkedin.com/in/vaishnavi-dayanand-85864524a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
                
We believe in data-driven insights and user-friendly tools that make complex analytics accessible to everyone.


    """)
    st.markdown("</div>", unsafe_allow_html=True)

st.sidebar.success("Select a page above.")
