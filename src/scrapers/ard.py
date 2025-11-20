import requests
import json
import re
from src.scrapers.base_scraper import PodcastScraper

class ARDScraper(PodcastScraper):
    def fetch_latest(self):
        base_url = "https://www.ardaudiothek.de/sendung/quarks-daily-dein-taeglicher-wissenspodcast/urn:ard:show:08a8bbd2f74c3824/"
        print(f"Checking ARD ({base_url})...")
        
        try:
            # 1. Get Page to find ID
            res = requests.get(base_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            
            # Look for identifier in ld+json
            match = re.search(r'"identifier":"(\d+)"', res.text)
            if not match:
                # Fallback: try to find programSetId in other scripts
                match = re.search(r'"programSetId":(\d+)', res.text)
            
            if match:
                program_id = match.group(1)
                api_url = f"https://api.ardaudiothek.de/programsets/{program_id}"
                print(f"Found ID: {program_id}, fetching API: {api_url}")
                
                api_res = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                data = api_res.json()['data']['programSet']
                
                items = data.get('items', {}).get('nodes', [])
                results = []
                
                for item in items[:3]:
                    title = item.get('title')
                    audio_url = None
                    if 'audios' in item and len(item['audios']) > 0:
                        audio_url = item['audios'][0]['url']
                    
                    image_url = None
                    if 'image' in item and 'url' in item['image']:
                        image_url = item['image']['url'].replace('{width}', '1280')
                        
                    source_url = f"https://www.ardaudiothek.de/episode/{item.get('id')}"
                    
                    if audio_url:
                        results.append({
                            "title": title,
                            "image_url": image_url,
                            "audio_url": audio_url,
                            "source_url": source_url
                        })
                return results
            else:
                print("Could not find ARD Program ID")
                return []
                
        except Exception as e:
            print(f"Error scraping ARD: {e}")
            return []