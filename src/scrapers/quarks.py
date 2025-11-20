import requests
from src.scrapers.base_scraper import PodcastScraper

class QuarksScraper(PodcastScraper):
    def fetch_latest(self):
        # Quarks Daily is on ARD Audiothek with ID 72680234
        # Using the API is more reliable than the WDR feed which has SSL issues often.
        program_id = "72680234"
        api_url = f"https://api.ardaudiothek.de/programsets/{program_id}"
        print(f"Checking Quarks via ARD API ({api_url})...")
        
        try:
            api_res = requests.get(api_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if api_res.status_code != 200:
                print(f"Error fetching Quarks API: {api_res.status_code}")
                return []
                
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
        except Exception as e:
            print(f"Error scraping Quarks: {e}")
            return []
