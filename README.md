# 🎬 Video Downloader

**Video Downloader** is a Python application that allows you to download videos from **YouTube**, **Twitch**, and **Kick**.

When a direct download is not available (especially on Kick), the app intelligently reconstructs the real stream URL and downloads it automatically.

---

## ✨ Features

- 🎥 **Download videos from:**
  - YouTube
  - Twitch
  - Kick
- ⚡ **Automatic fallback for Kick:**
  - Detects when direct download fails
  - Reconstructs the real `.m3u8` stream URL
  - Uses parallel requests to find it faster
- 🚀 **Multithreaded stream search**
- 🎯 **Best quality download** using `yt-dlp`
- 🔄 **Automatic platform detection**

---

## 🧠 How It Works

The application processes the input URL and determines the platform:

- **YouTube / Twitch** → direct download via `yt-dlp`
- **Kick** → advanced recovery system

### 🔹 Kick Recovery System

When a Kick download fails:

1. Retrieve channel data using `KickAPI`
2. Locate the video using its `uuid`
3. Extract:
   - `channel_id`
   - `video_id`
   - `start_time`
4. Generate multiple possible stream URLs
5. Test them in parallel
6. Return the first valid stream

### ⚡ Parallelism

The app uses Python threading to speed up stream discovery:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=10) as executor:
```

**What it does:**
- Sends multiple HTTP requests at the same time
- Reduces waiting time drastically
- Stops immediately when a valid stream is found

---

## 🚀 Installation

Install dependencies:

```bash
pip install yt-dlp kickapi cloudscraper
```

### 🔧 Required

Make sure `ffmpeg` is installed and available in PATH:

```bash
ffmpeg -version
```

---

## ▶️ Usage

Run the application:

```bash
python main.py
```

Enter a video URL:

```
Video URL: https://kick.com/...
```

### 🔄 Example Flow (Kick)

```
Attempt direct download
        ↓
      Fails
        ↓
Search video via API
        ↓
Generate possible URLs
        ↓
 Test in parallel
        ↓
Find valid stream
        ↓
Download with yt-dlp
```

---

## 📁 Project Structure

```
.
├── main.py
├── downloader.py
└── README.md
```

---

## ⚠️ Notes

- Kick does not always provide direct video URLs
- Streams are reconstructed manually
- Not all videos may be accessible
- The method may break if Kick changes its system

---

## 🧩 Future Improvements

- [ ] Support more platforms
- [ ] GUI interface
- [ ] Manual quality selection
- [ ] Stream URL caching
- [ ] Async version (`aiohttp`)

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| `yt-dlp` | Video downloading |
| `KickAPI` | Retrieve video metadata |
| `cloudscraper` | Bypass protections |
| `ffmpeg` | Media processing |
| `concurrent.futures` | Multithreading |

---

## 📌 Example Output

```
Video URL: https://kick.com/user/video/123

kick.com --> Kick
Trying another way...
Searching Videos...
Searching URL...
Found URL: https://stream.kick.com/...
Downloading...
```
