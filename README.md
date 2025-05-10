<p align="center">
  <!-- Replace with the path/URL of your banner or logo image -->
  <img src="https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202203/face-600x900.png" alt="FaceMatcher banner" width="300">
</p>

# FaceMatcher 😎🔍

**Detect, visualize 🖼️, and compare 🆚 faces in a flash!**

---

## ✨ Features

| Emoji | Capability |
| :---: | --- |
| 🔍 | **Face detection** in a single image |
| 🖼️ | **Bounding-box visualization** (optional `--show`) |
| 🔄 | **Face comparison** between two images |
| ⚙️ | **Simple CLI** with sensible defaults (`detect` / `compare`) |

---

## 📦 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/facematcher.git
   cd facematcher
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## 🛠️ Prerequisites
🐍 Python 3.8+

☁️ Google Cloud project with Vision API enabled

🔑 Service-account JSON key

## Usage

### 🔍 Detect Faces

To detect faces in an image:

```bash
facematcher detect --image photo.jpg --show
```

The `--show` flag is optional and will display the image with bounding boxes around detected faces.

### 🔄 Compare Faces

To compare faces between two images:

```bash
facematcher compare --image-a alice.jpg --image-b bob.jpg
```

You can adjust the matching threshold (lower is stricter) with the `--threshold` option:

```bash
facematcher compare --image-a alice.jpg --image-b bob.jpg --threshold 50.0
```

### 🔑 Credentials

Either set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

Or specify the credentials file path with the `--credentials` option:

```bash
facematcher detect --image photo.jpg --credentials /path/to/your/credentials.json
```

## 🧑‍💻 Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## 📄 License

MIT License - see LICENSE file for details 
