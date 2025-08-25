import feedparser
import requests
import time
import json
import os

# Telegram bilgileri (Render'da Environment Variables olarak ekleyeceğiz)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Haber kaynakları (birden fazla ekleyebilirsin)
RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.wired.com/feed/rss",
    "https://www.theverge.com/rss/index.xml"
]

SENT_FILE = "sent_news.json"

def load_sent():
    try:
        with open(SENT_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()

def save_sent(sent):
    with open(SENT_FILE, "w") as f:
        json.dump(list(sent), f)

def send_message(text):
    payload = {"chat_id": CHAT_ID, "text": text}
    requests.post(URL, data=payload)

if __name__ == "__main__":
    sent = load_sent()
    while True:
        for rss in RSS_FEEDS:
            feed = feedparser.parse(rss)
            for entry in feed.entries:
                if entry.link not in sent:
                    msg = f"📰 {entry.title}\n{entry.link}"
                    send_message(msg)
                    sent.add(entry.link)
                    save_sent(sent)
        time.sleep(300)  # her 5 dakikada bir kontrol et
