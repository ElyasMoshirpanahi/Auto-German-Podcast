# Auto-German-Podcast
![alt text](https://i0.wp.com/pedagogiaparaconcurseiros.com.br/wp-content/uploads/2020/08/podcast-logo.jpg?fit=1000%2C800&ssl=1)

This is a Python automation tool designed to fetch the latest science podcasts and educational videos from various German sources and broadcast them to a Telegram channel.

**Live Demo:** <a href='https://t.me/+y7-l2vGlTFQ2Njg0'>Telegram Channel</a>

## Features

*   **Multi-Source Scraping:**
    *   **Spektrum.de:** Fetches science podcasts across multiple categories.
    *   **Podigee:** Scrapes RSS feeds for "Zehn Minuten Alltagswissen".
    *   **Quarks Daily & ARD Audiothek:** Retrieves high-quality daily science content via API.
    *   **YouTube Integration:** Occasionally fetches and processes fun educational videos (e.g., *Dinge Erklärt – Kurzgesagt*, *Simplicissimus*) with German subtitles.
*   **Smart Processing:**
    *   **Audio Splitting:** Automatically splits large audio files to fit within Telegram's limits.
    *   **Video Compression:** Compresses videos to <20MB to ensure smooth delivery on mobile and strict adherence to data limits.
    *   **Subtitle Burning:** Automatically downloads and burns German subtitles into YouTube videos for better accessibility.
*   **Database Tracking:** Uses MongoDB to prevent duplicate posts.
*   **Automated Deployment:** Runs on GitHub Actions via Cron schedule.

## Setup

### Prerequisites
1.  **Python 3.10+**
2.  **FFmpeg:** Essential for audio/video processing.
3.  **MongoDB:** A database instance (e.g., MongoDB Atlas).
4.  **Telegram Bot:** A bot token and channel ID.

### Installation

1.  Clone the repo:
    ```bash
    git clone https://github.com/ElyasMoshirpanahi/Auto-German-Podcast
    cd Auto-German-Podcast
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
Create a `.env` file or set the following environment variables:

```bash
BOT_TOKEN=your_telegram_bot_token
CHANNEL_ID=your_channel_id
MONGODB_URI=your_mongodb_connection_string
```

## Usage

**Run the main script:**
```bash
python -m src.main
```

**Test specific sources (Dry Run):**
```bash
python -m src.main --dry-run --test-source youtube
```

## Architecture
The project is modularized into:
*   `src/scrapers/`: Individual modules for each content source.
*   `src/services/`: Helper services for Telegram, Audio, and Video processing.
*   `src/main.py`: The central orchestrator.

## License
Feel free to fork and modify!