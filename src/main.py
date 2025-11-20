import os
import sys
import argparse
import random
from src.config import TMP_DIR
from src.database import Database
from src.services.telegram import TelegramBot
from src.services.audio import AudioService
from src.services.video import VideoService
from src.scrapers.spektrum import SpektrumScraper
from src.scrapers.podigee import PodigeeScraper
from src.scrapers.quarks import QuarksScraper
from src.scrapers.ard import ARDScraper
from src.scrapers.youtube import YoutubeScraper

# Ensure tmp dir exists
os.makedirs(TMP_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Auto German Podcast")
    parser.add_argument("--dry-run", action="store_true", help="Do not download/send, just check.")
    parser.add_argument("--test-source", type=str, help="Test a specific source (spektrum, podigee, quarks, ard, youtube)")
    args = parser.parse_args()

    db = Database()
    bot = TelegramBot()
    audio_service = AudioService()
    video_service = VideoService()

    scrapers = {
        "spektrum": SpektrumScraper(),
        "podigee": PodigeeScraper(),
        "quarks": QuarksScraper(),
        "ard": ARDScraper()
    }
    
    # Regular Podcast Scrapers
    target_scrapers = {}
    run_youtube = False

    if args.test_source:
        if args.test_source == "youtube":
            run_youtube = True
        elif args.test_source in scrapers:
            target_scrapers = {args.test_source: scrapers[args.test_source]}
        else:
            print(f"Unknown source: {args.test_source}")
            return
    else:
        target_scrapers = scrapers
        # Occasional YouTube feature: 30% chance
        if random.random() < 0.3:
            run_youtube = True

    # 1. Run Standard Podcast Scrapers
    for name, scraper in target_scrapers.items():
        print(f"\n--- Running Scraper: {name} ---")
        results = scraper.fetch_latest()
        
        if not results:
            print("No episodes found.")
            continue

        for episode in results:
            title = episode['title']
            audio_url = episode['audio_url']
            image_url = episode['image_url']
            source_url = episode['source_url']

            print(f"Found: {title}")

            if db.exists(title):
                print(f"Skipping (Already processed): {title}")
                continue

            if args.dry_run:
                print(f"[Dry Run] Would process: {title} from {audio_url}")
                continue

            # Process
            print(f"Processing new episode: {title}")
            
            # Download
            safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
            filename = os.path.join(TMP_DIR, f"{safe_title[:30].replace(' ', '_')}.mp3")
            
            downloaded_file = audio_service.download(audio_url, filename)
            
            if not downloaded_file:
                db.add(title, audio_url, status="broken", log="Download failed")
                continue

            # Split
            files_to_send = audio_service.split_if_needed(downloaded_file)

            # Send Banner
            if image_url:
                bot.send_photo(image_url, caption=f"<b>{title}</b>\nSource: {source_url}")
            else:
                bot.send_message(f"<b>{title}</b>\nSource: {source_url}")

            # Send Audio(s)
            for f_path in files_to_send:
                bot.send_audio(f_path, caption=title)
                try: os.remove(f_path)
                except: pass

            if downloaded_file and downloaded_file not in files_to_send and os.path.exists(downloaded_file):
                 try: os.remove(downloaded_file)
                 except: pass

            db.add(title, audio_url, status="posted")
            print(f"Successfully processed: {title}")

    # 2. Run YouTube Scraper (Occasional)
    if run_youtube:
        print("\n--- Running Scraper: youtube ---")
        yt_scraper = YoutubeScraper()
        results = yt_scraper.fetch_latest()
        
        for video in results:
            title = video['title']
            url = video['audio_url'] # YT URL
            
            print(f"Found YT: {title}")
            
            if db.exists(title):
                print(f"Skipping YT (Already processed): {title}")
                continue
                
            if args.dry_run:
                print(f"[Dry Run] Would process YT: {title} from {url}")
                break # Only process one YT video max
                
            print(f"Processing new YT video: {title}")
            
            # Download
            safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
            base_filename = os.path.join(TMP_DIR, f"yt_{safe_title[:20].replace(' ', '_')}")
            
            video_path, sub_path = yt_scraper.download_video(url, base_filename)
            
            if not video_path or not os.path.exists(video_path):
                print("Failed to download video.")
                db.add(title, url, status="broken", log="YT Download failed")
                continue

            final_video = video_path
            
            # Burn Subs if available
            if sub_path:
                burned_path = video_path.replace(".mp4", "_subbed.mp4")
                if video_service.burn_subtitles(video_path, sub_path, burned_path):
                    final_video = burned_path
                    # Remove original
                    try: os.remove(video_path)
                    except: pass
                    try: os.remove(sub_path)
                    except: pass
            
            # Compress if > 20MB (User Constraint)
            # Check size
            size_mb = os.path.getsize(final_video) / (1024*1024)
            if size_mb > 19.5:
                compressed_path = final_video.replace(".mp4", "_compressed.mp4")
                if video_service.compress_video(final_video, compressed_path, target_size_mb=19):
                     # Remove uncompressed
                    try: os.remove(final_video)
                    except: pass
                    final_video = compressed_path
                else:
                    print("Compression failed. Sending as is (might fail if > 50MB).")
            
            # Send
            bot.send_video(final_video, caption=f"<b>{title}</b>\nSource: {url}")
            
            # Cleanup
            try: os.remove(final_video)
            except: pass
            
            db.add(title, url, status="posted")
            print(f"Successfully processed YT: {title}")
            break # Only 1 video per run

if __name__ == "__main__":
    main()