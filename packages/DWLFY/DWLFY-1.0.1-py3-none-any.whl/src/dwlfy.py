import os
import re
import logging
import hashlib
import sqlite3
import subprocess
import shutil


# Configuração de logs
logging.basicConfig(
    format='Date-Time : %(asctime)s : Line No. : %(lineno)d - %(message)s',
    level=logging.DEBUG,
    filename='../log/app.dmp',
    filemode='a'
)


# ==========================
# Cache Manager
# ==========================
class CacheManager:
    def __init__(self, db_path="../cache/cache.db"):
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self._setup_database()

    def _setup_database(self):
        if not os.path.exists(self.db_path):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS downloads (video_id TEXT PRIMARY KEY, nome TEXT, path TEXT)"
                    )
                    conn.commit()
                logging.info("Database setup completed.")
            except sqlite3.Error as e:
                logging.error("Database setup failed: %s", e)

    def _generate_video_id(self, nome):
        return hashlib.sha256(nome.encode()).hexdigest()

    def has_downloaded(self, nome):
        video_id = self._generate_video_id(nome)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT path FROM downloads WHERE video_id = ?", (video_id,))
                result = cursor.fetchone()
                return result[0] if result else None
        except sqlite3.Error as e:
            logging.error("Error checking if video is downloaded: %s", e)
            return None

    def store_download(self, nome, path):
        video_id = self._generate_video_id(nome)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO downloads (video_id, nome, path) VALUES (?, ?, ?)",
                    (video_id, nome, path)
                )
                conn.commit()
                logging.info("Stored download info for video_id %s", video_id)
        except sqlite3.Error as e:
            logging.error("Error storing download info: %s", e)


# ==========================
# YouTube URL Validator
# ==========================
class YouTubeURLValidator:
    YOUTUBE_REGEX = re.compile(
        r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})", re.IGNORECASE
    )

    def __init__(self, verify_exists=False, user_agent='Mozilla/5.0'):
        self.verify_exists = verify_exists
        self.user_agent = user_agent

    def __call__(self, url):
        return bool(self.YOUTUBE_REGEX.match(url))


# ==========================
# Downloader
# ==========================
class Downloader:
    def __init__(self, cache_manager=None):
        self.cache_manager = cache_manager or CacheManager()

    def execute_command(self, command):
        try:
            logging.info(f"Executing: {' '.join(command)}")
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error executing command: {e}")
        except Exception as e:
            logging.error(f"General error: {e}")

    def move_downloaded_file(self, download_dir, destination):
        try:
            for file_name in os.listdir(download_dir):
                if file_name.endswith(('.mp4', '.webm')):
                    full_file_path = os.path.join(download_dir, file_name)
                    destination_file = os.path.join(destination, file_name)
                    os.makedirs(destination, exist_ok=True)
                    shutil.move(full_file_path, destination_file)
                    return destination_file
            logging.warning("No video file found to move.")
            return None
        except Exception as e:
            logging.error(f"Error moving file: {e}")
            return None

    def download_video(self, url, download_dir = "downloads", destination = "", format_option="best", height=None):
        if not YouTubeURLValidator()(url):
            logging.error("Invalid YouTube URL.")
            return

        video_name = f"{url.split('=')[-1]}"
        cached_path = self.cache_manager.has_downloaded(video_name)

        if cached_path:
            logging.info(f"Video already downloaded: {cached_path}")
            return cached_path

        command = [
            "yt-dlp", "-f", format_option, url,
            "-o", f"{download_dir}/%(title)s.%(ext)s"
        ]

        if height:
            command.insert(3, f"height<={height}")

        self.execute_command(command)
        downloaded_file_path = self.move_downloaded_file(download_dir, destination)

        if downloaded_file_path:
            self.cache_manager.store_download(video_name, downloaded_file_path)

        return downloaded_file_path

    def download_and_convert(self, url, download_dir, destination, conversion_format="mp3"):
        video_file_path = self.download_video(url, download_dir, destination, format_option="worst")

        if video_file_path is None:
            logging.error("No video file downloaded.")
            return

        base_name = os.path.splitext(os.path.basename(video_file_path))[0]
        target_file_path = os.path.join(destination, f"{base_name}.{conversion_format}")

        try:
            os.makedirs(destination, exist_ok=True)
            conversion_command = ["ffmpeg", "-i", video_file_path, "-f", conversion_format, target_file_path]
            self.execute_command(conversion_command)
            self.cache_manager.store_download(url, target_file_path)
            os.remove(video_file_path)
        except Exception as e:
            logging.error(f"Error converting file: {e}")


# ==========================
# Execução Principal
# ==========================
# if __name__ == "__main__":
#     downloader = Downloader()
#     downloader.download_video(
#         url="https://www.youtube.com/watch?v=SkwVvdf2F_Q&t=1321s",
#         destination="/home/lucas/Downloads/downloaded",
#     )
    # downloader.download_and_convert(
    #     url="https://www.youtube.com/watch?v=SkwVvdf2F_Q&t=1321s",
    #     download_dir="downloads",
    #     destination="/home/lucas/Downloads/dowloaded",
    #     conversion_format="mp3"
    # )
