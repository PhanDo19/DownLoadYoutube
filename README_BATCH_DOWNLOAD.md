# YouTube Video Downloader - Batch Download Feature

## Overview
This YouTube video downloader now supports downloading multiple videos from a list of URLs, in addition to single video downloads.

## New Features

### 1. Batch Download from URL List
- Download multiple YouTube videos at once
- Simply paste a list of URLs (one per line) in the text area
- Automatic validation of YouTube URLs
- Progress tracking for each video
- Error handling for individual failed downloads

### 2. Enhanced GUI
- **Single Video Tab**: Download individual videos or playlists
- **Batch Download Tab**: Download multiple videos from a list
- Clear status updates during downloads
- Helper buttons for managing URL lists

## How to Use Batch Download

### Step 1: Open the Application
Run the application and you'll see two sections:
- "Tải video đơn lẻ" (Single Video Download)
- "Tải nhiều video từ danh sách URL" (Batch Download from URL List)

### Step 2: Prepare Your URL List
In the batch download section, paste your YouTube URLs in the text area. Format:
```
https://youtu.be/VIDEO_ID1
https://youtu.be/VIDEO_ID2
https://www.youtube.com/watch?v=VIDEO_ID3
https://youtube.com/watch?v=VIDEO_ID4
```

### Step 3: Use Helper Buttons
- **"Tải URL mẫu"**: Load sample URLs for testing
- **"Xóa danh sách"**: Clear the URL list
- **"Tải tất cả video"**: Start batch download

### Step 4: Monitor Progress
- Real-time status updates show current download progress
- See which video is being processed (X/Y format)
- Automatic error handling continues with remaining videos

### Step 5: View Results
After completion, you'll see a summary:
- Number of successfully downloaded videos
- Number of skipped videos (already downloaded)
- Number of failed downloads with error details

## Features

### URL Validation
- Automatically validates YouTube URLs
- Warns about invalid URLs before starting
- Option to continue with valid URLs only

### Duplicate Prevention
- Checks download history to avoid re-downloading
- Skips videos that were previously downloaded
- Maintains history in `history.txt`

### Error Handling
- Individual video failures don't stop the entire process
- Detailed error messages for troubleshooting
- Continues with remaining videos

### Download Quality
- Downloads best available quality
- Combines video and audio streams
- Outputs in MP4 format

## File Locations
- **Downloads**: `output/` folder
- **History**: `history.txt` file
- **FFmpeg**: `ffmpeg/bin/` folder (required for merging streams)

## Tips for Best Results

1. **Valid URLs**: Ensure all URLs are valid YouTube links
2. **Network**: Stable internet connection recommended for batch downloads
3. **Storage**: Check available disk space for multiple video downloads
4. **Patience**: Large batches may take considerable time

## Supported URL Formats
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## Example Usage
```
https://youtu.be/dQw4w9WgXcQ
https://youtu.be/L_jWHffIx5E
https://www.youtube.com/watch?v=9bZkp7q19f0
```

## Error Messages
- **"Không tìm thấy URL hợp lệ"**: No valid URLs found in the list
- **"URL không phải YouTube"**: Non-YouTube URLs detected
- **"Đã tải trước đó"**: Video already in download history
- **"Lỗi tải video"**: Download failed for specific video

## Requirements
- Python with yt-dlp library
- FFmpeg for video processing
- Stable internet connection
- Sufficient storage space
