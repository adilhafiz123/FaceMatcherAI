"""Setup configuration for facematcher package."""

from setuptools import setup, find_packages

setup(
    name="facematcher",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-cloud-vision>=3.0.0",
        "Pillow>=9.0.0",
        "matplotlib>=3.0.0",  # Optional, for visualization
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "facematcher=facematcher.__main__:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Face detection and matching utility using Google Cloud Vision API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/facematcher",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 