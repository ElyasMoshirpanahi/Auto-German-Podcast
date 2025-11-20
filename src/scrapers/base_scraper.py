from abc import ABC, abstractmethod

class PodcastScraper(ABC):
    @abstractmethod
    def fetch_latest(self):
        """
        Returns a list of dictionaries: 
        [
            {
                "title": str, 
                "image_url": str, 
                "audio_url": str, 
                "source_url": str
            }
        ]
        """
        pass
