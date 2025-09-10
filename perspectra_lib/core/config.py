"""Configuration for Perspectra library."""

from dataclasses import dataclass


@dataclass
class PerspectraConfig:
    """Configuration settings for Perspectra library."""

    # Padding settings
    padding_ratio: float = 0.05

    # Background removal model settings
    use_local_model: bool = True
    model_filename: str = "u2net.onnx"
    model_url: str = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
    is_only_mask: bool = True

    # Perspective transformation settings
    save_contours: bool = False
    contours_path: str = "debug_output"
    save_transformed: bool = False

    # ONNX Runtime settings
    ort_num_threads: int = 4
    ort_enable_cpu_mem_arena: int = 1
    ort_enable_mem_pattern: int = 1
    ort_enable_parallel_execution: int = 1
    ort_intra_op_num_threads: int = 4
    ort_inter_op_num_threads: int = 2
    ort_execution_mode: str = "PARALLEL"
    ort_graph_opt_level: str = "ALL"

    # Logging settings
    enable_logging: bool = True
    log_level: str = "INFO"
