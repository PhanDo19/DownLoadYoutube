# 🎬 Multi-Platform Video Downloader

A clean, organized GUI tool for downloading high-quality videos from **YouTube**, **TikTok**, and **Douyin**. Features a modern object-oriented design with comprehensive error handling and batch download capabilities.

## ✨ Key Features

- **🎯 Multi-Platform Support**: YouTube, TikTok, Douyin
- **📊 Quality Selection**: 720p (Fast), 1080p (Balanced), 1440p (High), 4K (Best), Auto, Best Available
- **📦 Batch Downloads**: Download multiple videos with parallel processing option
- **🔄 Smart Duplicate Detection**: Automatically skips previously downloaded videos
- **📝 Download History**: Complete tracking of downloaded videos
- **🍪 Cookie Support**: Optional browser cookie authentication for private videos
- **🎨 Clean Interface**: Modern, intuitive GUI design
- **🔧 Robust Error Handling**: Comprehensive fallback strategies

## 📁 Project Structure

```
DownLoadYoutube/
├── ffmpeg/
│   └── bin/
│       ├── ffmpeg.exe          # FFmpeg binary for video processing
│       ├── ffplay.exe          # Media player
│       └── ffprobe.exe         # Media information tool
├── output/                     # Downloaded videos storage
├── downloads/                  # Alternative download location
├── douyin_downloads/           # Douyin-specific downloads
├── douyin_videos/              # Douyin video cache
├── __pycache__/               # Python cache files
├── main.py                     # Main application (cleaned & organized)
├── requirements.txt            # Python dependencies
├── history.txt                 # Download history log
├── history.json               # Download history (JSON format)
└── README.md                  # This documentation
```

## ⚙️ System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows (PowerShell support)
- **Dependencies**: `yt-dlp` (latest version)
- **Optional**: FFmpeg (included for YouTube processing)

## 🚀 Quick Start

### 1. Install Python
Download from [python.org](https://www.python.org/downloads/)
> ⚠️ **Important**: Check "Add Python to PATH" during installation

### 2. Install Dependencies
```powershell
pip install yt-dlp
```

### 3. Run the Application
```powershell
python main.py
```

### 4. Start Downloading
1. Paste video URL from supported platforms
2. Select desired quality
3. Configure advanced options (optional)
4. Click "Download Video" or use batch download for multiple URLs

## 🎛️ User Interface Guide

### Quality Options
- **720p (Fast)**: Smaller file size, faster download
- **1080p (Balanced)**: Good quality-to-size ratio (recommended)
- **1440p (High)**: High quality for larger screens
- **4K (Best)**: Maximum quality, largest file size
- **Auto**: Automatically selects best quality based on video analysis
- **Best Available**: Downloads highest quality available

### Advanced Options
- **🍪 Use browser cookies**: Enable for private/age-restricted videos
  - Requires browser to be closed for cookie access
  - Supports Chrome, Edge, and Firefox

### Download Modes
1. **Single Video**: Download individual videos or playlists
2. **Batch Download**: 
   - Enter multiple URLs (one per line)
   - Option for parallel downloads (faster but uses more bandwidth)
   - Automatic duplicate detection

## 🌐 Supported Platforms & URLs

### YouTube
```
✅ Individual videos:
https://youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID

✅ Playlists:
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