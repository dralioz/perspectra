"""Configuration for Perspectra library."""

from dataclasses import dataclass
from typing import Tuple

# Available model configurations
MODEL_CONFIGS = {
    "u2net": {
        "filename": "u2net.onnx",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
        "size": (320, 320),
        "description": "Full U2-Net model (168MB, high accuracy, slower)"
    },
    "u2net_lite": {
        "filename": "u2net_lite.onnx",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net_lite.onnx",
        "size": (320, 320),
        "description": "Lite U2-Net model (~4MB, good accuracy, faster)"
    },
    "silueta": {
        "filename": "silueta.onnx",
        "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/silueta.onnx",
        "size": (320, 320),
        "description": "Silueta model (~43MB, optimized for objects)"
    },
    "custom": {
        "filename": "custom_model.onnx",
        "url": "",
        "size": (224, 224),
        "description": "Custom fine-tuned model"
    }
}


@dataclass
class PerspectraConfig:
    """Configuration for the Perspectra library."""

    # Basic settings
    enable_logging: bool = True
    log_level: str = "INFO"

    # Background removal settings
    is_only_mask: bool = False
    background_color: str = "white"  # "white", "transparent", or hex color

    # Performance mode selection
    use_ultrafast: bool = False  # Use OpenCV-based ultra-fast methods (1-10ms)
    use_optimized: bool = False  # Use optimized ONNX inference (100-500ms)
    # threshold, watershed, grabcut (for ultrafast)
    fast_method: str = "threshold"

    # Perspective correction settings
    gaussian_blur_ksize: int = 5
    canny_threshold1: int = 100
    canny_threshold2: int = 200
    min_contour_area: int = 1000
    epsilon_factor: float = 0.02

    # Image processing settings
    image_size: Tuple[int, int] = (320, 320)
    preserve_aspect_ratio: bool = True

    # Performance settings
    use_local_model: bool = True
    model_type: str = "u2net"  # u2net, u2net_lite, silueta, custom
    model_filename: str = "u2net.onnx"
    model_url: str = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

    # Debug and additional settings
    save_contours: bool = False
    output_debug_images: bool = False
    use_gpu: bool = False
    padding_ratio: float = 0.05
    save_transformed: bool = False
    contours_path: str = "debug_output"

    # ONNX Runtime settings
    ort_intra_op_num_threads: int = 1
    ort_inter_op_num_threads: int = 1
    ort_enable_mem_pattern: bool = True
    ort_enable_cpu_mem_arena: bool = True
    ort_execution_mode: str = "SEQUENTIAL"
    ort_graph_opt_level: str = "ALL"
