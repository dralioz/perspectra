"""Setup configuration for Perspectra library."""

from setuptools import setup, find_packages

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Read README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="perspectra",
    version="0.1.0",
    description="A Python library for background removal and perspective correction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Durmuş Ali Öztürk",
    author_email="durmusdali.dali@gmail.com",
    url="https://github.com/dralioz/perspectra",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="image-processing, background-removal, perspective-correction, computer-vision",
    project_urls={
        "Bug Reports": "https://github.com/dralioz/perspectra/issues",
        "Source": "https://github.com/dralioz/perspectra",
    },
)
