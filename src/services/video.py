import os
import ffmpeg
from hurry.filesize import size, si

class VideoService:
    def compress_video(self, input_path, output_path, target_size_mb=19):
        """
        Compress video to target size in MB.
        """
        if not os.path.exists(input_path):
            return False
            
        file_size = os.path.getsize(input_path)
        target_size_bytes = target_size_mb * 1024 * 1024
        
        if file_size <= target_size_bytes:
            # No compression needed, just copy or return original path?
            # We return original path as output if we didn't touch it, 
            # but the caller expects output_path to exist.
            # Let's just copy it or rename it if needed, or handle logic in caller.
            # Here we will just copy/move to ensure output_path is valid.
            import shutil
            shutil.copy(input_path, output_path)
            return True

        # Calculate bitrate
        probe = ffmpeg.probe(input_path)
        duration = float(probe['format']['duration'])
        
        # Target bitrate (bits/s) = (target_size (bits) / duration)
        # Audio bitrate is usually ~128k.
        audio_bitrate = 128 * 1024 # 128 kbps
        target_total_bitrate = (target_size_bytes * 8) / duration
        target_video_bitrate = target_total_bitrate - audio_bitrate
        
        print(f"Compressing {input_path} ({size(file_size)}) to {target_size_mb}MB...")
        print(f"Duration: {duration}s, Target Video Bitrate: {target_video_bitrate/1024:.0f}k")

        if target_video_bitrate < 100000: # < 100kbps is too low
            print("Warning: Target bitrate is extremely low. Video might be unwatchable.")

        try:
            # Two-pass encoding usually better but slower. Single pass with CRF is unpredictable for exact size.
            # We'll use constrained quality or average bitrate. 
            # Using average bitrate with buffer to hit size.
            
            (
                ffmpeg
                .input(input_path)
                .output(output_path, video_bitrate=target_video_bitrate, audio_bitrate=audio_bitrate)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return True
        except ffmpeg.Error as e:
            print(f"FFmpeg Error: {e.stderr.decode()}")
            return False
        except Exception as e:
            print(f"Compression Error: {e}")
            return False

    def burn_subtitles(self, video_path, sub_path, output_path):
        """
        Burn subtitles into video.
        """
        print(f"Burning subtitles from {sub_path} into {video_path}...")
        try:
            # Note: 'subtitles' filter requires the subtitle file path. 
            # Windows paths in ffmpeg filters can be tricky (need escaping).
            # Using simplified approach.
            
            # Check if sub file exists
            if not os.path.exists(sub_path):
                print("Subtitle file not found.")
                return False

            # Use ffmpeg-python
            video = ffmpeg.input(video_path)
            audio = video.audio
            
            # Prepare subtitle path for filter (escape backslashes for Windows)
            # ffmpeg needs forward slashes or escaped backslashes
            safe_sub_path = sub_path.replace('\\', '/').replace(':', '\\:')
            
            # Simple burn
            stream = ffmpeg.filter(video, 'subtitles', safe_sub_path)
            
            out = ffmpeg.output(stream, audio, output_path)
            out.run(overwrite_output=True, quiet=True)
            return True
        except ffmpeg.Error as e:
            print(f"FFmpeg Subtitle Error: {e.stderr.decode() if e.stderr else e}")
            return False
        except Exception as e:
            print(f"Subtitle Burn Error: {e}")
            return False
