import requests
from bs4 import BeautifulSoup
import random
from src.scrapers.base_scraper import PodcastScraper

class SpektrumScraper(PodcastScraper):
    def fetch_latest(self):
        themes = ['astronomie','biologie','chemie','erde-umwelt','technik','medizin','physik','psychologie-hirnforschung']
        random_theme = random.choice(themes)
        url = f"https://www.spektrum.de/podcast/{random_theme}/"
        print(f"Checking Spektrum ({random_theme})...")
        
        try:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.findAll("article")
            
            results = []
            for article in articles[:3]: # Check first 3
                try:
                    title = article.text.split(":")[-1].strip()
                    link_tag = list(article.children)[-1]
                    image_url = link_tag.findAll("img")[0]['src']
                    source_url = f"https://www.spektrum.de{link_tag['href']}"
                    
                    # Resolve Audio Link (Deep dive)
                    audio_url = self._grab_audio_link(source_url)
                    
                    if audio_url:
                        results.append({
                            "title": title,
                            "image_url": image_url,
                            "audio_url": audio_url,
                            "source_url": source_url
                        })
                except Exception as e:
                    print(f"Error parsing spektrum article: {e}")
                    continue
            
            return results
        except Exception as e:
            print(f"Error scraping Spektrum: {e}")
            return []

    def _grab_audio_link(self, url):
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            
            # Method 1: Direct MP3 link in script
            scripts = soup.find_all("script")
            for s in scripts:
                if ".mp3" in str(s):
                    import re
                    matches = re.findall('(?<=/)[\w\-\_]+\.mp3', str(s))
                    if matches:
                        return "https://cdn.podigee.com/media/" + matches[0]
            
            # Method 2: Iframe
            frames = soup.find_all("iframe")
            for f in frames:
                if "embed" in f.get('src', ''):
                    r2 = requests.get(f['src'])
                    soup2 = BeautifulSoup(r2.content, 'html.parser')
                    for a in soup2.find_all("a", href=True):
                        if ".mp3" in str(a):
                            return a["href"]
        except:
            return None
        return None
