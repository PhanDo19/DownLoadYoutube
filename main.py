import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
from yt_dlp import YoutubeDL
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

FFMPEG_DIR = os.path.join("ffmpeg", "bin")
OUTPUT_DIR = "output"
HISTORY_FILE = "history.txt"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global variables for progress tracking
current_download_progress = 0
total_downloads = 0
current_video_title = ""

def progress_hook(d):
    """Progress hook for yt-dlp to track download progress"""
    global current_download_progress, current_video_title
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d['total_bytes']:
            percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
            current_download_progress = percent
            current_video_title = d.get('filename', '').split('\\')[-1] if '\\' in d.get('filename', '') else d.get('filename', '')
        elif '_percent_str' in d:
            try:
                percent_str = d['_percent_str'].strip('%')
                current_download_progress = float(percent_str)
            except:
                pass
    elif d['status'] == 'finished':
        current_download_progress = 100
        current_video_title = d.get('filename', '').split('\\')[-1] if '\\' in d.get('filename', '') else d.get('filename', '')

def save_to_history_txt(video_title, video_url):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{video_title} | {video_url}\n")

def is_duplicate_download(video_url):
    if not os.path.exists(HISTORY_FILE):
        return False
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return any(video_url in line for line in f.readlines())

def get_video_urls(url):
    try:
        with YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'entries' in info:
                return [entry['webpage_url'] for entry in info['entries']]
            else:
                return [info['webpage_url']]
    except Exception as e:
        raise RuntimeError("Không lấy được danh sách video: " + str(e))

def get_optimized_format(quality_choice):
    """Get optimized format string based on quality choice"""
    if quality_choice == "720p":
        return 'best[height<=720][ext=mp4]/best[height<=720]/best[ext=mp4]/best'
    elif quality_choice == "1080p":
        return 'best[height<=1080][ext=mp4]/best[height<=1080]/best[ext=mp4]/best'
    else:  # best
        return 'best[ext=mp4]/bestvideo+bestaudio/best'

def download_single_video_threaded(url, video_index, total_videos):
    """Download a single video with optimized settings"""
    try:
        quality_choice = quality_var.get()
        format_selector = get_optimized_format(quality_choice)
        
        ydl_opts = {
            # Optimized format selection based on user choice
            'format': format_selector,
            'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_DIR,
            
            # Performance optimizations
            'concurrent_fragments': 4,  # Moderate concurrency to avoid overwhelming
            'retries': 2,  # Reduce retries for faster failure handling
            'fragment_retries': 2,
            'skip_unavailable_fragments': False,
            
            # Network optimizations
            'http_chunk_size': 2097152,  # 2MB chunks for better download speed
            'buffersize': 1048576,  # 1MB buffer
            
            # Skip unnecessary operations for speed
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writedescription': False,
            'writethumbnail': False,
            'writeinfojson': False,
            
            # Faster extraction
            'extract_flat': False,
            'lazy_playlist': True,
            'ignoreerrors': True,  # Continue on errors
            
            # Suppress verbose output for better performance
            'quiet': True,
            'no_warnings': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')
            save_to_history_txt(title, info.get('webpage_url', url))
            return {
                'success': True,
                'filename': f"{title}.{ext}",
                'url': url,
                'index': video_index
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'url': url,
            'index': video_index
        }

def download_best_video(url):
    try:
        quality_choice = quality_var.get()
        format_selector = get_optimized_format(quality_choice)
        
        ydl_opts = {
            # Optimized format selection for better performance
            'format': format_selector,
            'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
            'ffmpeg_location': FFMPEG_DIR,
            
            # Performance optimizations
            'concurrent_fragments': 6,  # Download fragments concurrently
            'retries': 2,  # Reduce retries for faster failure handling
            'fragment_retries': 2,
            'skip_unavailable_fragments': False,
            
            # Network optimizations
            'http_chunk_size': 2097152,  # 2MB chunks for better download speed
            'buffersize': 1048576,  # 1MB buffer
            
            # Skip unnecessary operations for speed
            'writesubtitles': False,
            'writeautomaticsub': False,
            'writedescription': False,
            'writethumbnail': False,
            'writeinfojson': False,
            
            # Faster extraction
            'extract_flat': False,
            'lazy_playlist': True,
            
            # Progress hook for better UI feedback
            'progress_hooks': [progress_hook],
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            ext = info.get('ext', 'mp4')
            save_to_history_txt(title, info.get('webpage_url', url))
            return f"{title}.{ext}"
    except Exception as e:
        raise RuntimeError("Lỗi tải video: " + str(e))

def is_valid_youtube_url(url):
    """Check if URL is a valid YouTube URL"""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url.lower() for domain in youtube_domains)

def download_from_url_list():
    urls_text = url_list_entry.get("1.0", tk.END).strip()
    if not urls_text:
        messagebox.showerror("Lỗi", "Vui lòng nhập danh sách URL")
        return

    # Parse URLs from text area
    all_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    if not all_urls:
        messagebox.showerror("Lỗi", "Không tìm thấy URL hợp lệ")
        return

    # Validate YouTube URLs
    valid_urls = [url for url in all_urls if is_valid_youtube_url(url)]
    invalid_urls = [url for url in all_urls if not is_valid_youtube_url(url)]
    
    if invalid_urls:
        invalid_count = len(invalid_urls)
        if messagebox.askyesno("URL không hợp lệ", 
                              f"Tìm thấy {invalid_count} URL không phải YouTube.\n"
                              f"Bạn có muốn tiếp tục với {len(valid_urls)} URL hợp lệ?"):
            urls = valid_urls
        else:
            return
    else:
        urls = valid_urls

    if not urls:
        messagebox.showerror("Lỗi", "Không có URL YouTube hợp lệ")
        return

    # Filter out already downloaded URLs
    urls_to_download = [url for url in urls if not is_duplicate_download(url)]
    skipped_count = len(urls) - len(urls_to_download)

    if not urls_to_download:
        messagebox.showinfo("Thông báo", "Tất cả video đã được tải trước đó!")
        return

    # Ask for parallel downloads
    use_parallel = messagebox.askyesno("Tùy chọn tải", 
                                     f"Tải {len(urls_to_download)} video.\n"
                                     f"Bạn có muốn tải song song (nhanh hơn nhưng tốn băng thông)?")

    # Disable UI during download
    btn_download_list.config(state='disabled')
    btn_download.config(state='disabled')
    
    def download_worker():
        try:
            global total_downloads
            total_downloads = len(urls_to_download)
            downloaded = []
            failed = []
            
            if use_parallel:
                # Parallel download with limited workers to avoid overwhelming
                max_workers = min(3, len(urls_to_download))  # Max 3 parallel downloads
                
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # Submit all download tasks
                    future_to_url = {
                        executor.submit(download_single_video_threaded, url, idx, len(urls_to_download)): url 
                        for idx, url in enumerate(urls_to_download, 1)
                    }
                    
                    # Process completed downloads
                    for future in as_completed(future_to_url):
                        result = future.result()
                        
                        if result['success']:
                            downloaded.append(result['filename'])
                            status_text = f"Hoàn thành {len(downloaded)}/{len(urls_to_download)}: {result['filename'][:30]}..."
                        else:
                            failed.append(f"{result['url']}: {result['error']}")
                            status_text = f"Lỗi {len(failed)}/{len(urls_to_download)}: {result['url'][:30]}..."
                        
                        # Update UI in main thread
                        root.after(0, lambda text=status_text: status_label.config(text=text))
                        root.after(0, root.update)
            else:
                # Sequential download
                for idx, url in enumerate(urls_to_download, start=1):
                    status_text = f"Đang tải video {idx}/{len(urls_to_download)}: {url[:50]}..."
                    root.after(0, lambda text=status_text: status_label.config(text=text))
                    root.after(0, root.update)
                    
                    try:
                        filename = download_best_video(url)
                        downloaded.append(filename)
                    except Exception as e:
                        failed.append(f"{url}: {str(e)}")
                        continue

            # Show results
            message = f"Tải thành công {len(downloaded)} video."
            if skipped_count:
                message += f"\nBỏ qua {skipped_count} video đã tải trước đó."
            if failed:
                message += f"\nLỗi {len(failed)} video."
                if len(failed) <= 3:  # Show details for few failures
                    message += "\nChi tiết lỗi:\n" + "\n".join(failed[:3])

            root.after(0, lambda: messagebox.showinfo("Hoàn tất", message))
            root.after(0, lambda: status_label.config(text="Hoàn tất!"))
            
        except Exception as e:
            root.after(0, lambda: status_label.config(text="Đã xảy ra lỗi."))
            root.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
        finally:
            # Re-enable UI
            root.after(0, lambda: btn_download_list.config(state='normal'))
            root.after(0, lambda: btn_download.config(state='normal'))

    # Start download in background thread
    threading.Thread(target=download_worker, daemon=True).start()
    status_label.config(text="Đang bắt đầu tải danh sách video...")

def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Lỗi", "Vui lòng nhập link YouTube")
        return

    # Disable UI during download
    btn_download.config(state='disabled')
    btn_download_list.config(state='disabled')

    def download_worker():
        try:
            status_label.config(text="Đang phân tích liên kết...")
            root.update()

            video_urls = get_video_urls(url)
            downloaded = []
            skipped = []
            failed = []
            
            for idx, v_url in enumerate(video_urls, start=1):
                status_text = f"Đang tải video {idx}/{len(video_urls)}..."
                root.after(0, lambda text=status_text: status_label.config(text=text))
                root.after(0, root.update)
                
                try:
                    if is_duplicate_download(v_url):
                        skipped.append(v_url)
                        continue
                    filename = download_best_video(v_url)
                    downloaded.append(filename)
                except Exception as e:
                    failed.append(f"{v_url}: {str(e)}")
                    continue

            message = f"Tải thành công {len(downloaded)} video."
            if skipped:
                message += f"\nBỏ qua {len(skipped)} video đã tải trước đó."
            if failed:
                message += f"\nLỗi {len(failed)} video."

            root.after(0, lambda: messagebox.showinfo("Hoàn tất", message))
            root.after(0, lambda: status_label.config(text="Hoàn tất!"))
            
        except Exception as e:
            root.after(0, lambda: status_label.config(text="Đã xảy ra lỗi."))
            root.after(0, lambda: messagebox.showerror("Lỗi", str(e)))
        finally:
            # Re-enable UI
            root.after(0, lambda: btn_download.config(state='normal'))
            root.after(0, lambda: btn_download_list.config(state='normal'))

    # Start download in background thread
    threading.Thread(target=download_worker, daemon=True).start()

def view_download_history():
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo("Lịch sử", "Chưa có video nào được tải.")
        return
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        history = f.read()
    messagebox.showinfo("Lịch sử tải", history)

def clear_url_list():
    url_list_entry.delete("1.0", tk.END)

def load_sample_urls():
    sample_urls = """https://youtu.be/vA47xcdzQAA
https://youtu.be/mc7I8h7Ahao
https://youtu.be/4MRou53tYFk
https://youtu.be/Uu8l1c0pzmY
https://youtu.be/fH8nq7sFDbs"""
    url_list_entry.delete("1.0", tk.END)
    url_list_entry.insert("1.0", sample_urls)

# GUI đơn giản
root = tk.Tk()
root.title("YouTube Best Quality Downloader")
root.geometry("640x480")

# Create notebook for tabs
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Add quality selection frame
quality_frame = tk.LabelFrame(main_frame, text="Tùy chọn chất lượng (ảnh hưởng tốc độ tải)", font=("Arial", 10, "bold"))
quality_frame.pack(fill=tk.X, pady=(0, 10))

quality_var = tk.StringVar(value="720p")
quality_options = [
    ("720p (Nhanh nhất)", "720p"),
    ("1080p (Cân bằng)", "1080p"),
    ("Tốt nhất (Chậm nhất)", "best")
]

tk.Label(quality_frame, text="Chọn chất lượng video:").pack(side=tk.LEFT, padx=5)
for text, value in quality_options:
    tk.Radiobutton(quality_frame, text=text, variable=quality_var, value=value).pack(side=tk.LEFT, padx=5)

# Single URL tab
single_frame = tk.LabelFrame(main_frame, text="Tải video đơn lẻ", font=("Arial", 10, "bold"))
single_frame.pack(fill=tk.X, pady=(0, 10))

tk.Label(single_frame, text="Nhập link video hoặc danh sách phát:").pack(pady=5)
url_entry = tk.Entry(single_frame, width=70)
url_entry.pack(pady=5)

btn_download = tk.Button(single_frame, text="Tải video chất lượng tốt nhất", command=start_download)
btn_download.pack(pady=10)

# Multiple URLs tab
multi_frame = tk.LabelFrame(main_frame, text="Tải nhiều video từ danh sách URL", font=("Arial", 10, "bold"))
multi_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

tk.Label(multi_frame, text="Nhập danh sách URL (mỗi URL một dòng):").pack(pady=5)
url_list_entry = scrolledtext.ScrolledText(multi_frame, width=70, height=8)
url_list_entry.pack(pady=5, fill=tk.BOTH, expand=True)

# Add placeholder text
placeholder_text = """https://youtu.be/example1
https://youtu.be/example2
https://youtu.be/example3"""
url_list_entry.insert("1.0", placeholder_text)

# Button frame for URL list controls
url_list_btn_frame = tk.Frame(multi_frame)
url_list_btn_frame.pack(pady=5)

btn_download_list = tk.Button(url_list_btn_frame, text="Tải tất cả video", command=download_from_url_list, bg="green", fg="white")
btn_download_list.pack(side=tk.LEFT, padx=5)

btn_clear_list = tk.Button(url_list_btn_frame, text="Xóa danh sách", command=clear_url_list)
btn_clear_list.pack(side=tk.LEFT, padx=5)

btn_sample_urls = tk.Button(url_list_btn_frame, text="Tải URL mẫu", command=load_sample_urls)
btn_sample_urls.pack(side=tk.LEFT, padx=5)

# History and status
control_frame = tk.Frame(main_frame)
control_frame.pack(fill=tk.X)

btn_history = tk.Button(control_frame, text="Xem lịch sử đã tải", command=view_download_history)
btn_history.pack(side=tk.LEFT)

status_label = tk.Label(main_frame, text="", fg="blue")
status_label.pack(pady=5)

root.mainloop()
