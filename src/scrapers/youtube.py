import yt_dlp
import os
import glob
import random
from src.scrapers.base_scraper import PodcastScraper
from src.config import TMP_DIR

class YoutubeScraper(PodcastScraper):
    def __init__(self):
        self.search_queries = [
            "ytsearch5:Dinge Erklärt – Kurzgesagt",
            "ytsearch5:Simplicissimus",
            "ytsearch5:MrWissen2go"
        ]
    
    def fetch_latest(self):
        # Randomly pick a query
        query = random.choice(self.search_queries)
        print(f"Searching YouTube: {query}...")
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True, # Don't download, just list
        }
        
        results = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                if 'entries' in info:
                    for entry in info['entries']:
                        # Filter: Duration (skip very long videos > 15 mins)
                        duration = entry.get('duration', 0)
                        if duration and duration > 900: 
                            continue
                            
                        results.append({
                            "title": entry['title'],
                            "image_url": entry.get('thumbnails', [{}])[-1].get('url') if 'thumbnails' in entry else None,
                            "audio_url": entry['url'], # This is the YT video URL
                            "source_url": entry['url'],
                            "is_youtube": True,
                            "duration": duration
                        })
        except Exception as e:
            print(f"Error fetching YouTube info: {e}")
            
        return results

    def download_video(self, url, output_base):
        """
        Download video and german subtitles.
        Returns (video_path, subtitle_path)
        """
        print(f"Downloading YouTube video: {url}")
        
        # Output template
        out_tmpl = f"{output_base}.%(ext)s"
        
        ydl_opts = {
            'format': 'best[ext=mp4][height<=480]/best[ext=mp4]', # 480p max to save size
            'outtmpl': out_tmpl,
            'writesubtitles': True,
            'subtitleslangs': ['de', 'de-orig'], # Prefer German
            'writeautomaticsub': True, # Fallback to auto-subs
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Find the files
            # Video is likely .mp4
            video_path = f"{output_base}.mp4"
            if not os.path.exists(video_path):
                 # fallback search
                 files = glob.glob(f"{output_base}*.mp4")
                 if files: video_path = files[0]
                 else: return None, None

            # Subtitle is likely .de.vtt or .vtt
            sub_path = None
            possible_subs = glob.glob(f"{output_base}*.vtt")
            if possible_subs:
                sub_path = possible_subs[0] # Take first found
            
            return video_path, sub_path
            
        except Exception as e:
            print(f"YT Download Error: {e}")
            return None, None
