import feedparser
from src.scrapers.base_scraper import PodcastScraper

class PodigeeScraper(PodcastScraper):
    def fetch_latest(self):
        url = "https://zehnminutenalltagswissen.podigee.io/feed/mp3"
        print(f"Checking Podigee ({url})...")
        return self._parse_feed(url)

    def _parse_feed(self, feed_url):
        try:
            feed = feedparser.parse(feed_url)
            results = []
            for entry in feed.entries[:3]:
                audio_url = None
                # Check links for audio
                for link in entry.links:
                    if 'audio' in link.type:
                        audio_url = link.href
                        break
                
                if audio_url:
                    results.append({
                        "title": entry.title,
                        "image_url": feed.feed.image.href if hasattr(feed.feed, 'image') else None,
                        "audio_url": audio_url,
                        "source_url": entry.link
                    })
            return results
        except Exception as e:
            print(f"Error parsing feed {feed_url}: {e}")
            return []
