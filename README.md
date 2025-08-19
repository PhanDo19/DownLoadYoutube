# 🎬 YouTube Best Quality Downloader

A simple GUI tool for downloading high-quality videos from **YouTube**, supporting both individual videos and playlists. The tool automatically avoids duplicate downloads and saves download history for easy tracking.

## 📁 Directory Structure

```
youtube_best_downloader/
├── ffmpeg/bin/ffmpeg.exe    ← Local FFmpeg binary (required)
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

### Step 3: Setup FFmpeg
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract `ffmpeg.exe` to: `ffmpeg/bin/ffmpeg.exe`

## 🚀 Usage

1. Run `python main.py`
2. Paste YouTube video or playlist link
3. Click "Download Best Quality Video"
4. Videos save to `output/` folder

## 🧠 Features

✅ Downloads highest quality videos with FFmpeg merging  
✅ Supports individual videos and playlists  
✅ Automatic duplicate detection  
✅ Download history tracking  
✅ User-friendly GUI


