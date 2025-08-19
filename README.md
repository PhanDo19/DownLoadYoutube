# 🎬 Multi-Platform Video Downloader

A simple GUI tool for downloading high-quality videos from **YouTube**, **Douyin**, and **TikTok**, supporting both individual videos and playlists. The tool automatically avoids duplicate downloads and saves download history for easy tracking.

## 📁 Directory Structure

```
video_downloader/
├── ffmpeg/bin/ffmpeg.exe    ← Local FFmpeg binary (required for YouTube)
├── output/                  ← Downloaded videos storage
├── main.py                  ← Main program file
└── README.md
```

## ⚙️ Requirements

- Python 3.7+
- `yt_dlp` library
- `tkinter` (included with Python)

## 🧩 Installation

### Step 1: Install Python
Download from: https://www.python.org/downloads/
*Remember to check "Add Python to PATH"*

### Step 2: Install Dependencies
```bash
pip install yt-dlp
```

### Step 3: Setup FFmpeg (for YouTube only)
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract `ffmpeg.exe` to: `ffmpeg/bin/ffmpeg.exe`

## 🚀 Usage

1. Run `python main.py`
2. Paste video link from supported platforms:
   - **YouTube**: Video or playlist link
   - **TikTok**: Individual video link
   - **Douyin**: Individual video link
3. Select quality (720p/1080p/Best)
4. Click "Download Best Quality Video"
5. Videos save to `output/` folder

## 🧠 Features

✅ **Multi-Platform Support**: YouTube, TikTok, Douyin  
✅ **Quality Selection**: 720p (fastest), 1080p (balanced), Best (slowest)  
✅ **Batch Downloads**: Download multiple videos from different platforms  
✅ **Smart Platform Detection**: Automatically optimizes settings per platform  
✅ **Duplicate Prevention**: Automatic duplicate detection  
✅ **Download History**: Track all downloaded videos  
✅ **User-friendly GUI**: Clean, intuitive interface

## 🌐 Supported Platforms

### YouTube
- Individual videos and playlists
- All quality options with FFmpeg merging
- Format: MP4 output

### TikTok / Douyin
- Individual videos
- Best available quality
- Direct download (no FFmpeg required)
- Format: Original platform format

## 📝 Supported URL Formats

```
YouTube:
- https://youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- https://youtube.com/playlist?list=PLAYLIST_ID

TikTok:
- https://tiktok.com/@user/video/VIDEO_ID
- https://vm.tiktok.com/SHORT_ID
- https://vt.tiktok.com/SHORT_ID

Douyin:
- https://douyin.com/video/VIDEO_ID
- https://v.douyin.com/SHORT_ID
```


