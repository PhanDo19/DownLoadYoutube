# YouTube Video Downloader# 🎬 Multi-Platform Video Downloader



A clean, high-quality video downloader for YouTube with GUI interface.A clean, organized GUI tool for downloading high-quality videos from **YouTube**, **TikTok**, and **Douyin**. Features a modern object-oriented design with comprehensive error handling and batch download capabilities.



## ✨ Features## ✨ Key Features



- **High Quality Downloads**: Supports up to 1080p+ resolution with AAC audio- **🎯 Multi-Platform Support**: YouTube, TikTok, Douyin

- **Simple GUI**: Easy-to-use tkinter interface- **📊 Quality Selection**: 720p (Fast), 1080p (Balanced), 1440p (High), 4K (Best), Auto, Best Available

- **Batch Downloads**: Multiple videos simultaneously- **📦 Batch Downloads**: Download multiple videos with parallel processing option

- **Format Selection**: Choose from 720p, 1080p, 1440p, 4K, or Best quality- **🔄 Smart Duplicate Detection**: Automatically skips previously downloaded videos

- **Audio Compatibility**: AAC format for universal player support- **📝 Download History**: Complete tracking of downloaded videos

- **No Cookies Required**: Works without browser authentication for most videos- **🍪 Cookie Support**: Optional browser cookie authentication for private videos

- **🎨 Clean Interface**: Modern, intuitive GUI design

## 🚀 Quick Start- **🔧 Robust Error Handling**: Comprehensive fallback strategies



1. **Run the application**:## 📁 Project Structure

   ```bash

   python main.py```

   ```DownLoadYoutube/

├── ffmpeg/

2. **Select quality**: Choose "1080p" for best results│   └── bin/

│       ├── ffmpeg.exe          # FFmpeg binary for video processing

3. **Paste YouTube URL** and click Download│       ├── ffplay.exe          # Media player

│       └── ffprobe.exe         # Media information tool

4. **Results**: Videos saved to `output/` folder with high quality├── output/                     # Downloaded videos storage

├── downloads/                  # Alternative download location

## 📋 Quality Guide├── douyin_downloads/           # Douyin-specific downloads

├── douyin_videos/              # Douyin video cache

### Recommended Settings:├── __pycache__/               # Python cache files

- **Quality**: 1080p (gets best available up to 1080p)├── main.py                     # Main application (cleaned & organized)

- **Cookies**: Leave disabled (works great without them)├── requirements.txt            # Python dependencies

- **Format**: Auto-selected (video: H.264, audio: AAC)├── history.txt                 # Download history log

├── history.json               # Download history (JSON format)

### Expected Results:└── README.md                  # This documentation

- **720p videos**: Download at 1280x720 with AAC audio```

- **1080p videos**: Download at 1920x1080 with AAC audio  

- **File sizes**: ~150-300MB for 1-hour 1080p video## ⚙️ System Requirements

- **Compatibility**: Plays on all modern media players

- **Python**: 3.7 or higher

## 🔧 Requirements- **Operating System**: Windows (PowerShell support)

- **Dependencies**: `yt-dlp` (latest version)

- Python 3.8+- **Optional**: FFmpeg (included for YouTube processing)

- yt-dlp (latest)

- FFmpeg (included in project)## 🚀 Quick Start



## 📁 Project Structure### 1. Install Python

Download from [python.org](https://www.python.org/downloads/)

```> ⚠️ **Important**: Check "Add Python to PATH" during installation

DownLoadYoutube/

├── main.py              # Main application### 2. Install Dependencies

├── requirements.txt     # Dependencies```powershell

├── ffmpeg/bin/         # FFmpeg binariespip install yt-dlp

├── output/             # Downloaded videos```

└── README.md           # This file

```### 3. Run the Application

```powershell

## 🎯 How It Workspython main.py

```

1. **Auto-selects TV client** for YouTube access (bypasses restrictions)

2. **Prioritizes bestvideo+bestaudio** format for maximum quality### 4. Start Downloading

3. **Prefers AAC audio** over Opus for better compatibility1. Paste video URL from supported platforms

4. **Uses FFmpeg** to merge video and audio streams2. Select desired quality

5. **No authentication required** for most public videos3. Configure advanced options (optional)

4. Click "Download Video" or use batch download for multiple URLs

## 💡 Tips

## 🎛️ User Interface Guide

- **High quality works without cookies** - no need to close browsers

- **Enable cookies only for private videos** - most public videos work without them### Quality Options

- **Choose 1080p quality** - automatically selects best available format- **720p (Fast)**: Smaller file size, faster download

- **Let it auto-select formats** - optimized for quality and compatibility- **1080p (Balanced)**: Good quality-to-size ratio (recommended)

- **1440p (High)**: High quality for larger screens

## 🔧 Troubleshooting- **4K (Best)**: Maximum quality, largest file size

- **Auto**: Automatically selects best quality based on video analysis

### Video quality still low?- **Best Available**: Downloads highest quality available

- Try a different video (some videos only have low quality)

- Check if video is age-restricted or private### Advanced Options

- **🍪 Use browser cookies**: Enable for private/age-restricted videos

### Audio not working?  - Requires browser to be closed for cookie access

- Update your media player (newer players support AAC)  - Supports Chrome, Edge, and Firefox

- Try VLC Media Player for best compatibility

### Download Modes

### Download errors?1. **Single Video**: Download individual videos or playlists

- Check internet connection2. **Batch Download**: 

- Verify YouTube URL is correct and public   - Enter multiple URLs (one per line)

   - Option for parallel downloads (faster but uses more bandwidth)

## 🎉 Success Metrics   - Automatic duplicate detection



Since optimization:## 🌐 Supported Platforms & URLs

- **Quality improved**: 360p → 1080p+ (200% increase)

- **Audio compatibility**: Opus → AAC (universal support)### YouTube

- **User experience**: Complex setup → Simple one-click download```

- **Reliability**: Cookie dependency removed✅ Individual videos:

https://youtube.com/watch?v=VIDEO_ID

---https://youtu.be/VIDEO_ID



**Happy downloading!** 🚀✅ Playlists:
https://youtube.com/playlist?list=PLAYLIST_ID

✅ Features:
- All quality options with FFmpeg processing
- Cookie authentication for private videos
- Playlist support with individual video extraction
```

### TikTok
```
✅ Individual videos:
https://tiktok.com/@user/video/VIDEO_ID
https://vm.tiktok.com/SHORT_ID
https://vt.tiktok.com/SHORT_ID

✅ Features:
- Direct download in original format
- No FFmpeg required
- Optimized format selection
```

### Douyin
```
✅ Individual videos:
https://douyin.com/video/VIDEO_ID
https://v.douyin.com/SHORT_ID

✅ Features:
- Native format preservation
- Optimized download settings
- Platform-specific quality options
```

## 🔧 Technical Features

### Code Organization
- **Object-Oriented Design**: Clean `VideoDownloader` class structure
- **Modular Methods**: Separated functionality for better maintainability
- **Error Handling**: Comprehensive exception handling with user-friendly messages
- **Thread Safety**: Proper UI updates from background threads

### Download Engine
- **Multi-Format Fallback**: Automatic format selection with fallback strategies
- **Progress Tracking**: Real-time download progress display
- **Cookie Management**: Intelligent browser cookie extraction and handling
- **Platform Optimization**: Customized settings for each supported platform

### Performance Features
- **Parallel Downloads**: Configurable concurrent download workers
- **Fragment Retry**: Automatic retry for failed download fragments
- **Smart Timeouts**: Optimized timeout settings for different scenarios
- **Memory Management**: Efficient handling of large video files

## 📋 Troubleshooting

### Common Issues

**"FFmpeg not found" warning**
- FFmpeg is included in the `ffmpeg/bin/` directory
- Only affects YouTube downloads
- TikTok/Douyin downloads work without FFmpeg

**Cookie database errors**
- Close all browser windows before downloading private videos
- Disable cookie authentication in settings if not needed
- Use different browser if current one is locked

**Download failures**
- Check internet connection
- Verify URL format is supported
- Try different quality settings
- Check if video is geo-restricted or private

**Slow downloads**
- Use lower quality settings (720p) for faster downloads
- Disable parallel downloads for unstable connections
- Check available bandwidth

### Error Messages Guide

| Error | Solution |
|-------|----------|
| "Invalid URL" | Ensure URL is from YouTube, TikTok, or Douyin |
| "Cookie database locked" | Close browser and retry |
| "Video unavailable" | Check if video is deleted or geo-restricted |
| "All formats failed" | Try different quality setting or check internet |

## 📊 File Formats & Quality

### Output Formats
- **YouTube**: MP4 (merged video+audio with FFmpeg)
- **TikTok**: Original format (usually MP4)
- **Douyin**: Original format (usually MP4)

### Quality Guidelines
- **720p**: ~1-3 MB/minute, good for mobile devices
- **1080p**: ~3-8 MB/minute, recommended for most use cases
- **1440p**: ~8-15 MB/minute, great for large screens
- **4K**: ~15-50 MB/minute, maximum quality for professional use

## 🔄 Version History

### Current Version (Cleaned)
- ✅ Refactored codebase with object-oriented design
- ✅ Removed redundant test and emergency files
- ✅ Improved error handling and user feedback
- ✅ Consolidated documentation
- ✅ Enhanced code organization and readability
- ✅ Optimized download performance

### Previous Improvements
- Multi-platform support implementation
- Cookie authentication system
- Batch download functionality
- Progress tracking and status updates
- Advanced quality selection options

## 📜 License & Usage

This tool is for personal use and educational purposes. Please respect platform terms of service and copyright laws when downloading content.

## 🤝 Contributing

The codebase is now clean and well-organized. Key areas for potential improvements:
- Additional platform support
- Enhanced quality analysis
- GUI improvements
- Performance optimizations

---

**Ready to download?** Run `python main.py` and start enjoying high-quality video downloads! 🎬