import os
import sys
import argparse
from src.config import TMP_DIR
from src.database import Database
from src.services.telegram import TelegramBot
from src.services.audio import AudioService
from src.scrapers.spektrum import SpektrumScraper
from src.scrapers.podigee import PodigeeScraper
from src.scrapers.quarks import QuarksScraper
from src.scrapers.ard import ARDScraper

# Ensure tmp dir exists
os.makedirs(TMP_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description="Auto German Podcast")
    parser.add_argument("--dry-run", action="store_true", help="Do not download/send, just check.")
    parser.add_argument("--test-source", type=str, help="Test a specific source (spektrum, podigee, quarks, ard)")
    args = parser.parse_args()

    db = Database()
    bot = TelegramBot()
    audio_service = AudioService()

    scrapers = {
        "spektrum": SpektrumScraper(),
        "podigee": PodigeeScraper(),
        "quarks": QuarksScraper(),
        "ard": ARDScraper()
    }

    if args.test_source:
        if args.test_source in scrapers:
            target_scrapers = {args.test_source: scrapers[args.test_source]}
        else:
            print(f"Unknown source: {args.test_source}")
            return
    else:
        target_scrapers = scrapers

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
            # Sanitize filename
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
                # Cleanup part
                try:
                    os.remove(f_path)
                except: pass

            # Cleanup original if it wasn't in files_to_send (i.e. it was split)
            if downloaded_file and downloaded_file not in files_to_send and os.path.exists(downloaded_file):
                 try:
                    os.remove(downloaded_file)
                 except: pass

            # Log success
            db.add(title, audio_url, status="posted")
            print(f"Successfully processed: {title}")

if __name__ == "__main__":
    main()
