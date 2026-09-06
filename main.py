import os
import requests
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# Web Server (Free Platform Uptime සඳහා)
app = Flask('')

@app.route('/')
def home():
    return "Movie Scraper Bot is Running Active!"

def run():
    app.run(host='0.0.0.0', port=3000)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# Movie Sites List
SITES = [
    {"name": "SinhalaSub", "url": "https://sinhalasub.lk/?s="},
    {"name": "CineSubz", "url": "https://cinesubz.lk/?s="},
    {"name": "Cineru", "url": "https://cineru.lk/?s="},
    {"name": "DubzoneLK", "url": "https://dubzonelk.com/?s="},
    {"name": "SinhalaCartoons", "url": "https://sinhalacartoons.com/?s="},
    {"name": "PupilVideo", "url": "https://pupilvideo.blogspot.com/search?q="},
    {"name": "SLMoviesHD", "url": "https://slmovieshd2020.blogspot.com/search?q="}
]

def search_movies(movie_query):
    found_results = []
    
    for site in SITES:
        try:
            target_url = f"{site['url']}{movie_query.replace(' ', '+')}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(target_url, headers=headers, timeout=5)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                elements = soup.find_all(['article', 'div', 'h2'], class_=['result-item', 'post', 'entry-title', 'post-title'])
                
                for el in elements:
                    link_tag = el.find('a') if el.name != 'a' else el
                    if link_tag and link_tag.text:
                        title = link_tag.text.strip()
                        url = link_tag.get('href')
                        
                        if movie_query.lower() in title.lower():
                            found_results.append({
                                "site": site['name'],
                                "title": title,
                                "link": url
                            })
        except Exception:
            continue
            
    return found_results

if __name__ == "__main__":
    keep_alive()
    print("Bot is ready. Enter movie command below:")
    
    while True:
        cmd = input("\nEnter command (e.g. .movie kungfu panda): ")
        if cmd.startswith(".movie "):
            query = cmd.replace(".movie ", "").strip()
            results = search_movies(query)
            
            if results:
                print(f"\n[✔] Result options found for '{query}':\n")
                for idx, item in enumerate(results, 1):
                    print(f"{idx}. [{item['site']}] {item['title']}")
                    print(f"   Link: {item['link']}")
            else:
                print("\n[✕] No results found on any listed site.")
