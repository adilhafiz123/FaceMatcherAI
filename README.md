# FaceMatcher

A Python utility for detecting faces in images and comparing whether faces match using the Google Cloud Vision API.

## Features

- Detect faces in images
- Visualize detected faces with bounding boxes
- Compare faces between two images
- Simple command-line interface

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/facematcher.git
   cd facematcher
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

## Prerequisites

- Python 3.8 or higher
- Google Cloud project with Vision API enabled
- Service account JSON key file

## Usage

### Detect Faces

To detect faces in an image:

```bash
facematcher detect --image photo.jpg --show
```

The `--show` flag is optional and will display the image with bounding boxes around detected faces.

### Compare Faces

To compare faces between two images:

```bash
facematcher compare --image-a alice.jpg --image-b bob.jpg
```

You can adjust the matching threshold (lower is stricter) with the `--threshold` option:

```bash
facematcher compare --image-a alice.jpg --image-b bob.jpg --threshold 50.0
```

### Google Cloud Credentials

Either set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
```

Or specify the credentials file path with the `--credentials` option:

```bash
facematcher detect --image photo.jpg --credentials /path/to/your/credentials.json
```

## Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## License

MIT License - see LICENSE file for details 