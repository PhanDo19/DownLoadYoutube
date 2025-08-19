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
- "Single Video Download" (Single Video Download)
- "Batch Download from URL List" (Batch Download from URL List)

### Step 2: Prepare Your URL List
In the batch download section, paste your YouTube URLs in the text area. Format:
```
https://youtu.be/VIDEO_ID1
https://youtu.be/VIDEO_ID2
https://www.youtube.com/watch?v=VIDEO_ID3
https://youtube.com/watch?v=VIDEO_ID4
```

### Step 3: Use Helper Buttons
- **"Load Sample URLs"**: Load sample URLs for testing
- **"Clear List"**: Clear the URL list
- **"Download All Videos"**: Start batch download

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

### Batch Download
- Download multiple YouTube videos simultaneously
- Paste URLs (one per line) in the text area
- Automatic URL validation and duplicate detection
- Progress tracking and error handling

### Quality Options
- Downloads best available quality
- Combines video and audio streams
- MP4 output format

## Supported URL Formats
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`

## Requirements
- Python with yt-dlp library
- FFmpeg for video processing
