import requests
from bs4 import BeautifulSoup
import json
import random
import time

# Proxy List 
proxies_list = [
    {"http": "http://username:password@proxy1:port", "https": "https://username:password@proxy1:port"},
    {"http": "http://username:password@proxy2:port", "https": "https://username:password@proxy2:port"},
    {"http": "http://proxy3:port", "https": "https://proxy3:port"}, 
]

# URL για αρχική σελίδα
start_url = "https://en.wikipedia.org/wiki/Special:Random"

# Scrape Function with Proxy Rotation
def scrape_wikipedia(url, proxies):
    proxy = random.choice(proxies)  # Επιλογή τυχαίου proxy
    try:
        response = requests.get(url, proxies=proxy, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h1', {'id': 'firstHeading'}).text
            content_div = soup.find('div', {'class': 'mw-parser-output'})
            paragraphs = content_div.find_all('p')
            content = "\n".join([p.text for p in paragraphs if p.text.strip()])
            return {"title": title, "url": url, "content": content}
        else:
            print(f"Non-200 response for {url}: {response.status_code}")
    except Exception as e:
        print(f"Error scraping {url} with proxy {proxy}: {e}")
    return None

# Συλλογή πολλών άρθρων
def collect_large_articles(proxies, max_articles=100):
    articles = []
    while len(articles) < max_articles:
        print(f"Scraping article {len(articles) + 1}/{max_articles}")
        article = scrape_wikipedia(start_url, proxies)
        if article:
            articles.append(article)
            print(f"Scraped: {article['title']}")
        time.sleep(random.uniform(1, 3))  # Αναμονή για αποφυγή μπλοκαρίσματος
    return articles

# Αποθήκευση σε JSON
def save_to_json(data, filename="large_wikipedia_articles.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(data)} articles to {filename}")

# Εφαρμογή
if __name__ == "__main__":
    articles = collect_large_articles(proxies_list, max_articles=200)  # Πάρε 200 άρθρα
    save_to_json(articles)
