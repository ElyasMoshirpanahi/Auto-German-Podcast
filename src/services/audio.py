import os
import requests
import math
from pydub import AudioSegment

class AudioService:
    def download(self, url, filename):
        print(f"Downloading {url} to {filename}...")
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return filename
        except Exception as e:
            print(f"Download error: {e}")
            if os.path.exists(filename):
                os.remove(filename)
            return None

    def split_if_needed(self, file_path, max_size_mb=19): # 19MB to be safe for 20MB limit
        if not os.path.exists(file_path):
            return []
            
        file_size = os.path.getsize(file_path) / (1024 * 1024)
        if file_size < max_size_mb:
            return [file_path]

        print(f"Splitting {file_path} ({file_size:.2f} MB)...")
        try:
            audio = AudioSegment.from_mp3(file_path)
            duration_ms = len(audio)
            
            parts = math.ceil(file_size / max_size_mb)
            segment_length_ms = duration_ms // parts
            
            files = []
            base_name = os.path.splitext(file_path)[0]
            
            for i in range(parts):
                start = i * segment_length_ms
                end = (i + 1) * segment_length_ms if i < parts - 1 else duration_ms
                segment = audio[start:end]
                part_name = f"{base_name}_part{i+1}.mp3"
                print(f"Exporting part {i+1}/{parts}: {part_name}")
                segment.export(part_name, format="mp3")
                files.append(part_name)
                
            return files
        except Exception as e:
            print(f"Error splitting audio: {e}")
            return [file_path] # Return original if split fails, might fail upload but better than crash
