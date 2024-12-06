import os
from moviepy import VideoFileClip
import yt_dlp

class YouTubeThumbnailExtractor:
    def __init__(self, output_path="thumbnails"):
        """
        Initialize the extractor with a default output directory.
        """
        self.output_path = output_path
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def extract_thumbnails(self, video_url, timestamps):
        """
        Extract thumbnails from a YouTube video at specified timestamps.

        Args:
            video_url (str): The URL of the YouTube video.
            timestamps (list of int): The timestamps (in seconds) to capture thumbnails.

        Returns:
            list: List of paths to the saved thumbnails.
        """
        # Set up yt-dlp to stream the video
        ydl_opts = {
            'format': 'best',
            'outtmpl': '-',  # Output to stdout, avoid downloading the file
            'noplaylist': True,  # Avoid downloading playlists
            'quiet': True,  # Reduce logs
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_url_stream = info_dict['url']

        # Load the video stream directly using moviepy
        clip = VideoFileClip(video_url_stream)

        thumbnail_paths = []
        for i, timestamp in enumerate(timestamps):
            if timestamp > clip.duration:
                print(f"Timestamp {timestamp} exceeds video duration {clip.duration}. Skipping.")
                continue

            # Save the frame at the timestamp
            frame_path = os.path.join(self.output_path, f"thumbnail_{i+1}.png")
            clip.save_frame(frame_path, t=timestamp)
            thumbnail_paths.append(frame_path)
            print(f"Thumbnail saved at {frame_path}")

        clip.close()
        return thumbnail_paths
