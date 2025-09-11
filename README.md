# Perspectra 🚀

**Ultra-fast Python library for background removal and perspective correction**

⚡ **200-1000x faster** than traditional deep learning models!  
🎯 **5ms processing time** vs 1000ms+ with U²-Net  
📄 **Perfect for documents**, photos, and real-time applications

## 🚀 Performance Highlights

| Method | Speed | Use Case | Quality | License |
|--------|-------|----------|---------|---------|
| **Watershed** | 9ms | Mixed backgrounds | ⭐⭐⭐⭐ | ✅ Apache 2.0 |
| **Threshold** | 104ms | Clean documents | ⭐⭐⭐ | ✅ Apache 2.0 |
| **GrabCut** | 236ms | Complex images | ⭐⭐⭐⭐⭐ | ✅ Apache 2.0 |
| **U²-Net Lite** | 831ms | Balanced quality | ⭐⭐⭐⭐ | ⚠️ Check model |
| **U²-Net** | 971ms | Research/High accuracy | ⭐⭐⭐⭐⭐ | ⚠️ Check model |
| **Silueta** | 819ms | Object-focused | ⭐⭐⭐⭐ | ⚠️ Check model |

✅ = Fully license-safe for commercial use  
⚠️ = Check model license requirements

This library provides easy-to-use tools for processing images by removing backgrounds and correcting perspective distortions.

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

## ⚡ Quick Start - Choose Your Method

### � Simple Method Selection

```python
from perspectra_lib import PerspectraProcessor, PerspectraConfig

# 🏃‍♂️ FASTEST - Real-time apps (9ms)
config = PerspectraConfig(background_method="watershed")

# 📄 DOCUMENTS - Clean backgrounds (104ms)  
config = PerspectraConfig(background_method="threshold")

# 🔥 HIGH QUALITY - Complex images (236ms)
config = PerspectraConfig(background_method="grabcut")

# 🧪 RESEARCH - Maximum accuracy (971ms)
config = PerspectraConfig(background_method="u2net")

# ⚖️ BALANCED - Good speed + quality (831ms)
config = PerspectraConfig(background_method="u2net_lite")

processor = PerspectraProcessor(config)

# Process image
success, error_msg, result_image, duration = processor.process_image_from_file("document.jpg")

if success:
    print(f"✅ Completed in {duration*1000:.1f}ms")
    processor.save_processed_image("input.jpg", "output.jpg")
else:
    print(f"❌ Error: {error_msg}")
```

### �️ Legacy Configuration (Still Supported)

```python
# Old way - still works for backward compatibility
config = PerspectraConfig(
    use_ultrafast=True,      # Enable ultra-fast mode  
    fast_method="threshold", # Specific ultra-fast method
    enable_logging=False     # Disable logging for speed
)
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
