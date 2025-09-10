# Perspectra Library

A Python library for background removal and perspective correction of images. This library provides easy-to-use tools for processing images by removing backgrounds and correcting perspective distortions.

## Features

- **Background Removal**: Remove backgrounds from images using advanced AI models
- **Perspective Correction**: Automatically detect and correct perspective distortions
- **Easy Configuration**: Flexible configuration options for different use cases
- **Multiple Output Formats**: Support for numpy arrays, base64 strings, and file outputs
- **Debug Support**: Optional debug image saving for development and troubleshooting

## Installation

```bash
pip install perspectra
```

## Quick Start

### Basic Usage

```python
from perspectra_lib import PerspectraProcessor

# Initialize the processor
processor = PerspectraProcessor()

# Process an image from file
success, error_msg, result_image, duration = processor.process_image_from_file("input.jpg")

if success:
    print(f"Processing completed in {duration:.2f} seconds")
    # result_image is a numpy array
else:
    print(f"Error: {error_msg}")

# Save processed image
success, error_msg, duration = processor.save_processed_image("input.jpg", "output.jpg")
```

### Advanced Configuration

```python
from perspectra_lib import PerspectraProcessor, PerspectraConfig

# Create custom configuration
config = PerspectraConfig(
    padding_ratio=0.1,  # 10% padding around detected object
    save_transformed=True,  # Save debug images
    contours_path="debug_output",  # Debug output directory
    log_level="DEBUG"  # Enable detailed logging
)

# Initialize processor with custom config
processor = PerspectraProcessor(config)

# Process image bytes
with open("input.jpg", "rb") as f:
    image_bytes = f.read()

success, error_msg, result_image, duration = processor.process_image(image_bytes)
```

### Working with Base64

```python
# Get result as base64 string
success, error_msg, result_base64, duration = processor.process_image_to_base64(image_bytes)

if success:
    # Use the base64 string (e.g., in web applications)
    print(f"Base64 result length: {len(result_base64)}")
```

## Configuration Options

The `PerspectraConfig` class provides the following configuration options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `padding_ratio` | float | 0.05 | Padding ratio around detected object (0.05 = 5%) |
| `use_local_model` | bool | True | Use local model files instead of downloading |
| `model_filename` | str | "u2net.onnx" | Name of the background removal model |
| `is_only_mask` | bool | True | Return only mask from background removal |
| `save_contours` | bool | False | Save contour detection debug images |
| `save_transformed` | bool | False | Save perspective transformation debug images |
| `contours_path` | str | "debug_output" | Directory for debug images |
| `enable_logging` | bool | True | Enable/disable logging |
| `log_level` | str | "INFO" | Logging level (DEBUG, INFO, WARNING, ERROR) |

## API Reference

### PerspectraProcessor

The main class for image processing.

#### Methods

- `process_image(image_bytes: bytes) -> Tuple[bool, str, Optional[np.ndarray], float]`
  - Process image from bytes
  - Returns: (success, error_message, result_image, duration)

- `process_image_to_base64(image_bytes: bytes) -> Tuple[bool, str, str, float]`
  - Process image and return as base64 string
  - Returns: (success, error_message, result_base64, duration)

- `process_image_from_file(image_path: str) -> Tuple[bool, str, Optional[np.ndarray], float]`
  - Process image from file path
  - Returns: (success, error_message, result_image, duration)

- `save_processed_image(image_path: str, output_path: str) -> Tuple[bool, str, float]`
  - Process image from file and save result
  - Returns: (success, error_message, duration)

## Requirements

- Python >= 3.8
- OpenCV >= 4.12.0
- PIL (Pillow) >= 11.3.0
- NumPy >= 1.21.0
- rembg >= 2.0.67
- onnxruntime >= 1.22.1

## License

MIT License. See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
