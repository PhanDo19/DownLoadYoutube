#!/usr/bin/env python3
"""
Multi-Platform Video Downloader
A clean, organized GUI tool for downloading videos from YouTube, TikTok, and Douyin.
"""

import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from yt_dlp import YoutubeDL
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import subprocess


class VideoDownloader:
    """Main video downloader class with all functionality organized"""
    
    def __init__(self):
        self.setup_paths()
        self.setup_globals()
        self.verify_ffmpeg()
    
    def setup_paths(self):
        """Initialize all file paths"""
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.ffmpeg_dir = os.path.join(self.current_dir, "ffmpeg", "bin")
        self.output_dir = os.path.join(self.current_dir, "output")
        self.history_file = os.path.join(self.current_dir, "history.txt")
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup_globals(self):
        """Initialize global variables for progress tracking"""
        self.current_download_progress = 0
        self.total_downloads = 0
        self.current_video_title = ""
    
    def verify_ffmpeg(self):
        """Check if FFmpeg is available"""
        ffmpeg_path = os.path.join(self.ffmpeg_dir, "ffmpeg.exe")
        if os.path.exists(ffmpeg_path):
            print(f"[OK] FFmpeg found at: {self.ffmpeg_dir}")
            self.has_ffmpeg = True
        else:
            print(f"[WARN] FFmpeg not found at: {ffmpeg_path}")
            self.has_ffmpeg = False

    # URL Validation Methods
    def is_valid_youtube_url(self, url):
        """Check if URL is a valid YouTube URL"""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        return any(domain in url.lower() for domain in youtube_domains)

    def is_valid_douyin_url(self, url):
        """Check if URL is a valid Douyin/TikTok URL"""
        douyin_domains = ['douyin.com', 'tiktok.com', 'vm.tiktok.com', 'vt.tiktok.com', 
                         'www.douyin.com', 'www.tiktok.com']
        return any(domain in url.lower() for domain in douyin_domains)

    def get_platform_type(self, url):
        """Determine the platform type from URL"""
        if self.is_valid_youtube_url(url):
            return 'youtube'
        elif self.is_valid_douyin_url(url):
            return 'douyin'
        else:
            return 'unknown'

    def is_valid_url(self, url):
        """Check if URL is valid for any supported platform"""
        return self.is_valid_youtube_url(url) or self.is_valid_douyin_url(url)

    # History Management Methods
    def save_to_history(self, video_title, video_url):
        """Save downloaded video to history"""
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(f"{video_title} | {video_url}\n")

    def is_duplicate_download(self, video_url):
        """Check if video has already been downloaded"""
        if not os.path.exists(self.history_file):
            return False
        with open(self.history_file, "r", encoding="utf-8") as f:
            return any(video_url in line for line in f.readlines())

    # Progress Tracking Methods
    def progress_hook(self, d):
        """Progress hook for yt-dlp to track download progress"""
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.current_download_progress = percent
            elif '_percent_str' in d:
                try:
                    percent_str = d['_percent_str'].strip('%')
                    self.current_download_progress = float(percent_str)
                except:
                    pass
            
            filename = d.get('filename', '')
            if '\\' in filename:
                self.current_video_title = filename.split('\\')[-1]
            else:
                self.current_video_title = filename
        
        elif d['status'] == 'finished':
            self.current_download_progress = 100
            filename = d.get('filename', '')
            if '\\' in filename:
                self.current_video_title = filename.split('\\')[-1]
            else:
                self.current_video_title = filename

    # Format Selection Methods

    # Format Selection Methods
    def get_format_for_quality(self, quality_choice, platform):
        """Get the appropriate format string based on quality choice and platform"""
        if platform == 'douyin':
            # Douyin/TikTok specific formats
            quality_map = {
                "720p": 'best[height<=720]/best',
                "1080p": 'best[height<=1080]/best',
                "1440p": 'best[height<=1440]/best',
                "4k": 'best[height<=2160]/best',
                "auto": 'best',
                "best": 'best'
            }
            return quality_map.get(quality_choice, 'best')
        
        else:  # YouTube - Use bestvideo+bestaudio for high quality
            # Map quality choices to format strings with AAC audio preference
            youtube_formats = {
                "720p": 'bestvideo[height<=720]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio',
                "1080p": 'bestvideo[height<=1080]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]',
                "1440p": 'bestvideo[height<=1440]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]',
                "4k": 'bestvideo+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]',
                "best": 'bestvideo+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]',
                "auto": 'bestvideo+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]'
            }
            return youtube_formats.get(quality_choice, 'bestvideo+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio[ext=m4a]')

    def get_download_options(self, format_selector):
        """Get platform-specific yt-dlp options"""
        base_opts = {
            'format': format_selector,
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'retries': 3,
            'fragment_retries': 3,
            'nocheckcertificate': True,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self.progress_hook],
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            },
        }
        
        # Set ffmpeg location if available
        if self.has_ffmpeg:
            base_opts['ffmpeg_location'] = self.ffmpeg_dir
            base_opts['merge_output_format'] = 'mp4'
            # Add audio conversion options for better compatibility
            base_opts['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }]
        
        return base_opts


    def _run_download(self, ydl_opts, url):
        """Execute download and return filename string."""
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')
            height = info.get('height', 'unknown')
            width = info.get('width', 'unknown')
            requested_formats = info.get('requested_formats', [])
            if requested_formats:
                for rf in requested_formats:
                    if rf.get('vcodec') != 'none':
                        height = rf.get('height', height)
                        width = rf.get('width', width)
                        break
            if height != 'unknown' and width != 'unknown':
                print(f"[OK] Downloaded: {width}x{height}")
            else:
                print(f"[OK] Downloaded: {title}")
            self.save_to_history(title, info.get('webpage_url', url))
            return f"{title}.{ext}"

    # Core Download Methods
    def download_single_video(self, url, quality_choice=None):
        """Download a single video with format fallback."""
        try:
            platform = self.get_platform_type(url)
            quality_choice = quality_choice or self.quality_var.get()
            print(f"[INFO] Downloading with quality: {quality_choice}")

            format_selector = self.get_format_for_quality(quality_choice, platform)
            fallback_formats = [
                format_selector,
                'best[height>=720]/best[height>=480]/best',
                'best'
            ]

            last_error = None
            for attempt, fmt in enumerate(fallback_formats):
                try:
                    return self._run_download(self.get_download_options(fmt), url)
                except Exception as e:
                    last_error = str(e)
                    print(f"[FAIL] Attempt {attempt + 1} failed: {last_error[:120]}...")
                    if attempt < len(fallback_formats) - 1:
                        time.sleep(1)

            raise RuntimeError(f"All formats failed. Last error: {last_error}")
        except Exception as e:
            raise RuntimeError(f"Download failed: {str(e)}")

    def get_video_urls(self, url):
        """Extract video URLs from playlists or single videos."""
        try:
            with YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                if 'entries' in info:
                    return [entry['webpage_url'] for entry in info['entries']]
                return [info['webpage_url']]
        except Exception as e:
            raise RuntimeError(f"Could not extract video URLs: {str(e)}")

    # GUI Event Handlers
    def start_download(self):
        """Handle single video download"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a video link")
            return
        
        if not self.is_valid_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube, TikTok, or Douyin URL")
            return

        quality_choice = self.quality_var.get()

        self.disable_ui()

        def download_worker():
            try:
                self.update_status("Analyzing link...")
                video_urls = self.get_video_urls(url)

                downloaded = []
                skipped = []
                failed = []

                for idx, v_url in enumerate(video_urls, start=1):
                    self.update_status(f"Downloading video {idx}/{len(video_urls)}...")

                    try:
                        if self.is_duplicate_download(v_url):
                            skipped.append(v_url)
                            continue
                        filename = self.download_single_video(v_url, quality_choice)
                        downloaded.append(filename)
                    except Exception as e:
                        failed.append(f"{v_url}: {str(e)}")
                        continue

                self.show_download_results(downloaded, skipped, failed)
                
            except Exception as e:
                self.show_error(f"Download failed: {str(e)}")
            finally:
                self.enable_ui()

        threading.Thread(target=download_worker, daemon=True).start()

    def download_from_url_list(self):
        """Handle batch download from URL list"""
        urls_text = self.url_list_entry.get("1.0", tk.END).strip()
        if not urls_text:
            messagebox.showerror("Error", "Please enter URL list")
            return

        all_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        if not all_urls:
            messagebox.showerror("Error", "No valid URLs found")
            return

        valid_urls = [url for url in all_urls if self.is_valid_url(url)]
        invalid_urls = [url for url in all_urls if not self.is_valid_url(url)]
        
        if invalid_urls:
            if not messagebox.askyesno("Invalid URLs", 
                                     f"Found {len(invalid_urls)} unsupported URLs.\n"
                                     f"Continue with {len(valid_urls)} valid URLs?"):
                return
        
        urls_to_download = [url for url in valid_urls if not self.is_duplicate_download(url)]
        skipped_count = len(valid_urls) - len(urls_to_download)

        if not urls_to_download:
            messagebox.showinfo("Info", "All videos have been downloaded previously!")
            return

        use_parallel = messagebox.askyesno("Download Options", 
                                         f"Download {len(urls_to_download)} videos.\n"
                                         f"Use parallel downloads (faster but uses more bandwidth)?")
        quality_choice = self.quality_var.get()

        self.disable_ui()

        def download_worker():
            try:
                self.total_downloads = len(urls_to_download)
                downloaded = []
                failed = []

                if use_parallel:
                    self.download_parallel(urls_to_download, downloaded, failed, quality_choice)
                else:
                    self.download_sequential(urls_to_download, downloaded, failed, quality_choice)

                self.show_download_results(downloaded, [], failed, skipped_count)
                
            except Exception as e:
                self.show_error(f"Batch download failed: {str(e)}")
            finally:
                self.enable_ui()

        threading.Thread(target=download_worker, daemon=True).start()

    def download_parallel(self, urls, downloaded, failed, quality_choice):
        """Download videos in parallel"""
        max_workers = min(3, len(urls))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.download_single_video, url, quality_choice): url
                for url in urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    filename = future.result()
                    downloaded.append(filename)
                    self.update_status(f"Completed {len(downloaded)}/{len(urls)}: {filename[:30]}...")
                except Exception as e:
                    failed.append(f"{url}: {str(e)}")
                    self.update_status(f"Failed {len(failed)}/{len(urls)}: {url[:30]}...")

    def download_sequential(self, urls, downloaded, failed, quality_choice):
        """Download videos one by one"""
        for idx, url in enumerate(urls, start=1):
            self.update_status(f"Downloading video {idx}/{len(urls)}: {url[:50]}...")
            try:
                filename = self.download_single_video(url, quality_choice)
                downloaded.append(filename)
            except Exception as e:
                failed.append(f"{url}: {str(e)}")

    # UI Helper Methods
    def disable_ui(self):
        """Disable UI buttons during download"""
        self.btn_download.config(state='disabled')
        self.btn_download_list.config(state='disabled')

    def enable_ui(self):
        """Re-enable UI buttons after download"""
        self.btn_download.config(state='normal')
        self.btn_download_list.config(state='normal')

    def update_status(self, message):
        """Update status label thread-safely"""
        self.root.after(0, lambda: self.status_label.config(text=message))
        self.root.after(0, self.root.update)

    def show_error(self, message):
        """Show error message thread-safely"""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.status_label.config(text="Error occurred"))

    def show_download_results(self, downloaded, skipped, failed, skipped_count=0):
        """Show download completion results"""
        message = f"Successfully downloaded {len(downloaded)} videos."
        if skipped:
            message += f"\nSkipped {len(skipped)} previously downloaded videos."
        if skipped_count:
            message += f"\nSkipped {skipped_count} previously downloaded videos."
        if failed:
            message += f"\nFailed {len(failed)} videos."
            if len(failed) <= 3:
                message += "\nError details:\n" + "\n".join(failed[:3])

        self.root.after(0, lambda: messagebox.showinfo("Completed", message))
        self.root.after(0, lambda: self.status_label.config(text="Completed!"))

    def view_download_history(self):
        """View download history"""
        if not os.path.exists(self.history_file):
            messagebox.showinfo("History", "No videos downloaded yet.")
            return
        
        with open(self.history_file, "r", encoding="utf-8") as f:
            history = f.read()
        messagebox.showinfo("Download History", history)

    def clear_url_list(self):
        """Clear the URL list text area"""
        self.url_list_entry.delete("1.0", tk.END)

    def load_sample_urls(self):
        """Load sample URLs for testing"""
        sample_urls = """https://youtu.be/dQw4w9WgXcQ
https://www.tiktok.com/@username/video/1234567890
https://v.douyin.com/example
https://youtu.be/9bZkp7q19f0"""
        self.url_list_entry.delete("1.0", tk.END)
        self.url_list_entry.insert("1.0", sample_urls)

    def update_progress_display(self):
        """Update progress display during downloads"""
        if self.current_video_title and self.current_download_progress > 0:
            progress_text = f"Downloading: {self.current_video_title[:30]}... ({self.current_download_progress:.1f}%)"
            self.status_label.config(text=progress_text)
        
        # Schedule next update
        self.root.after(1000, self.update_progress_display)

    def create_gui(self):
        """Create the main GUI"""
        self.root = tk.Tk()
        self.root.title("Multi-Platform Video Downloader - YouTube, TikTok, Douyin")
        self.root.geometry("760x620")

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Quality selection frame
        self.create_quality_frame(main_frame)
        
        # Single video download frame
        self.create_single_download_frame(main_frame)
        
        # Batch download frame
        self.create_batch_download_frame(main_frame)
        
        # Control and status frame
        self.create_control_frame(main_frame)

    def create_quality_frame(self, parent):
        """Create quality selection frame"""
        quality_frame = tk.LabelFrame(parent, text="Quality Options", font=("Arial", 10, "bold"))
        quality_frame.pack(fill=tk.X, pady=(0, 10))

        self.quality_var = tk.StringVar(value="1080p")
        quality_options = [
            ("720p (Fast)", "720p"),
            ("1080p (Balanced)", "1080p"),
            ("1440p (High)", "1440p"),
            ("4K (Best)", "4k"),
            ("Auto", "auto"),
            ("Best Available", "best")
        ]

        tk.Label(quality_frame, text="Select quality:").pack(side=tk.LEFT, padx=5)
        for text, value in quality_options:
            tk.Radiobutton(quality_frame, text=text, variable=self.quality_var, value=value).pack(side=tk.LEFT, padx=3)

    def create_single_download_frame(self, parent):
        """Create single video download frame"""
        single_frame = tk.LabelFrame(parent, text="Single Video Download", font=("Arial", 10, "bold"))
        single_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(single_frame, text="Enter YouTube, TikTok, or Douyin video/playlist link:").pack(pady=5)
        self.url_entry = tk.Entry(single_frame, width=70)
        self.url_entry.pack(pady=5)

        self.btn_download = tk.Button(single_frame, text="Download Video", 
                                     command=self.start_download, bg="green", fg="white")
        self.btn_download.pack(pady=10)

    def create_batch_download_frame(self, parent):
        """Create batch download frame"""
        multi_frame = tk.LabelFrame(parent, text="Batch Download", font=("Arial", 10, "bold"))
        multi_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tk.Label(multi_frame, text="Enter URLs (one per line):").pack(pady=5)
        self.url_list_entry = scrolledtext.ScrolledText(multi_frame, width=70, height=8)
        self.url_list_entry.pack(pady=5, fill=tk.BOTH, expand=True)

        # Button frame
        btn_frame = tk.Frame(multi_frame)
        btn_frame.pack(pady=5)

        self.btn_download_list = tk.Button(btn_frame, text="Download All", 
                                          command=self.download_from_url_list, bg="green", fg="white")
        self.btn_download_list.pack(side=tk.LEFT, padx=5)

        btn_clear = tk.Button(btn_frame, text="Clear List", command=self.clear_url_list)
        btn_clear.pack(side=tk.LEFT, padx=5)

        btn_sample = tk.Button(btn_frame, text="Load Sample URLs", command=self.load_sample_urls)
        btn_sample.pack(side=tk.LEFT, padx=5)

    def create_control_frame(self, parent):
        """Create control and status frame"""
        control_frame = tk.Frame(parent)
        control_frame.pack(fill=tk.X)

        btn_history = tk.Button(control_frame, text="View History", command=self.view_download_history)
        btn_history.pack(side=tk.LEFT)

        self.status_label = tk.Label(parent, text="Ready to download", fg="blue")
        self.status_label.pack(pady=5)
        
        # Add quality tips
        tips_label = tk.Label(parent, 
                            text="Tip: If YouTube says 'Sign in to confirm you are not a bot', use browser cookies from a browser that is signed in to YouTube.",
                            font=("Arial", 8), fg="gray", wraplength=600)
        tips_label.pack(pady=(0, 5))

    def run(self):
        """Run the application"""
        self.create_gui()
        self.update_progress_display()
        self.root.mainloop()


def main():
    """Main function to start the application"""
    app = VideoDownloader()
    app.run()


if __name__ == "__main__":
    main()
