"""Optimized background removal adapter for Perspectra library."""

import io
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image

from ..core.config import PerspectraConfig, MODEL_CONFIGS


class OptimizedBackgroundRemovalAdapter:
    """
    Optimized adapter for background removal with multiple model options
    and performance improvements.
    """

    def __init__(self, config: Optional[PerspectraConfig] = None):
        """
        Initialize the OptimizedBackgroundRemovalAdapter.

        Args:
            config: Configuration object. If None, uses default settings.
        """
        self.config = config or PerspectraConfig()

        # Setup logging
        if self.config.enable_logging:
            self.logger = logging.getLogger(__name__)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(getattr(logging, self.config.log_level))
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        # Setup model configuration
        self._setup_model_config()

        # Ensure model exists
        if self.config.use_local_model:
            self._ensure_model_exists()

        # Initialize ONNX session
        self.session = None
        self._initialize_onnx_session()

        self.logger.info(
            "OptimizedBackgroundRemovalAdapter initialized successfully.")

    def _setup_model_config(self):
        """Setup model configuration based on selected model type."""
        if self.config.model_type in MODEL_CONFIGS:
            model_config = MODEL_CONFIGS[self.config.model_type]
            self.model_dir = Path("models")
            self.model_path = self.model_dir / model_config["filename"]
            self.model_url = model_config["url"]
            self.input_size = model_config["size"]

            self.logger.info(f"Using model: {self.config.model_type}")
            self.logger.info(
                f"Model description: {model_config['description']}")
        else:
            # Fallback to config values
            self.model_dir = Path("models")
            self.model_path = self.model_dir / self.config.model_filename
            self.model_url = self.config.model_url
            self.input_size = self.config.image_size

    def _initialize_onnx_session(self):
        """Initialize ONNX Runtime session with optimizations."""
        if not self.model_path.exists():
            self.logger.warning(
                "Model file not found, session will be initialized on first use")
            return

        try:
            # Setup ONNX Runtime session options
            sess_options = ort.SessionOptions()
            sess_options.intra_op_num_threads = self.config.ort_intra_op_num_threads
            sess_options.inter_op_num_threads = self.config.ort_inter_op_num_threads
            sess_options.enable_mem_pattern = bool(
                self.config.ort_enable_mem_pattern)
            sess_options.enable_cpu_mem_arena = bool(
                self.config.ort_enable_cpu_mem_arena)

            # Set execution mode
            if self.config.ort_execution_mode == "PARALLEL":
                sess_options.execution_mode = ort.ExecutionMode.ORT_PARALLEL
            else:
                sess_options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL

            # Set graph optimization level
            optimization_levels = {
                "DISABLE": ort.GraphOptimizationLevel.ORT_DISABLE_ALL,
                "BASIC": ort.GraphOptimizationLevel.ORT_ENABLE_BASIC,
                "EXTENDED": ort.GraphOptimizationLevel.ORT_ENABLE_EXTENDED,
                "ALL": ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            }
            sess_options.graph_optimization_level = optimization_levels.get(
                self.config.ort_graph_opt_level,
                ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            )

            # Setup providers (CPU/GPU)
            providers = ['CPUExecutionProvider']
            if self.config.use_gpu:
                try:
                    providers.insert(0, 'CUDAExecutionProvider')
                    self.logger.info("GPU execution enabled")
                except Exception:
                    self.logger.warning("GPU not available, using CPU")

            # Create session
            self.session = ort.InferenceSession(
                str(self.model_path),
                sess_options=sess_options,
                providers=providers
            )

            self.logger.info("ONNX Runtime session initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize ONNX session: {e}")
            self.session = None

    def remove_background_optimized(self, image_bytes: bytes) -> np.ndarray:
        """
        Optimized background removal using direct ONNX inference.

        Args:
            image_bytes: The image data in bytes.

        Returns:
            The processed image as numpy array.
        """
        try:
            # Load and preprocess image
            original_image, input_tensor = self._load_and_preprocess_image(
                image_bytes)

            # Direct ONNX inference for speed
            if self.session is not None:
                mask = self._run_onnx_inference(original_image, input_tensor)
            else:
                # Fallback to rembg if ONNX session failed
                self.logger.warning("Using fallback rembg processing")
                return self._fallback_rembg_processing(image_bytes)

            # Post-process result
            result = self._postprocess_result(original_image, mask)

            return result

        except Exception as e:
            self.logger.error(f"Error in optimized background removal: {e}")
            # Fallback to original method
            return self._fallback_rembg_processing(image_bytes)

    def _load_and_preprocess_image(self, image_bytes: bytes) -> Tuple[np.ndarray, np.ndarray]:
        """Load and preprocess image for ONNX inference."""
        # Load original image
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        original = np.array(pil_image)

        # Resize for model input
        pil_resized = pil_image.resize(
            self.input_size, Image.Resampling.LANCZOS)
        resized = np.array(pil_resized)

        # Normalize to [0, 1] and transpose to CHW format
        normalized = resized.astype(np.float32) / 255.0
        input_tensor = normalized.transpose(2, 0, 1)[np.newaxis, ...]  # NCHW

        return original, input_tensor

    def _run_onnx_inference(
        self, original: np.ndarray, input_tensor: np.ndarray
    ) -> np.ndarray:
        """Run ONNX inference directly."""

        # Get input/output names
        input_name = self.session.get_inputs()[0].name
        output_name = self.session.get_outputs()[0].name

        # Run inference
        result = self.session.run([output_name], {input_name: input_tensor})

        # Process output
        mask = result[0][0, 0]  # Remove batch and channel dimensions

        # Resize mask back to original size
        # PIL size format
        original_size = (original.shape[1], original.shape[0])
        mask_resized = cv2.resize(
            mask, original_size, interpolation=cv2.INTER_LANCZOS4)

        # Threshold mask
        mask_binary = (mask_resized > 0.5).astype(np.uint8) * 255

        return mask_binary

    def _postprocess_result(self, original: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """Post-process the result."""
        # Convert mask to 3-channel
        if len(mask.shape) == 2:
            mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
        else:
            mask_3ch = mask

        # Apply mask to original image
        result = original.copy()
        result[mask_3ch < 128] = [255, 255, 255]  # White background

        return result

    def _fallback_rembg_processing(self, image_bytes: bytes) -> np.ndarray:
        """Fallback to original rembg processing."""
        try:
            from rembg import remove

            pil_image = Image.open(io.BytesIO(image_bytes))

            # Use rembg
            output_image = remove(
                image_bytes, only_mask=self.config.is_only_mask)
            image_rgb = Image.open(io.BytesIO(output_image)).convert("RGB")

            return np.array(image_rgb)

        except Exception as e:
            self.logger.error(f"Fallback processing failed: {e}")
            raise

    def _ensure_model_exists(self):
        """Download model if it doesn't exist."""
        if not self.model_dir.exists():
            self.logger.info("Models directory not found. Creating...")
            self.model_dir.mkdir(parents=True, exist_ok=True)

        if not self.model_path.exists() and self.model_url:
            try:
                self.logger.info(
                    f"Downloading {self.config.model_type} model from {self.model_url}")

                # Try curl first, then wget
                try:
                    subprocess.run(
                        ["curl", "-L", "-o",
                            str(self.model_path), self.model_url],
                        check=True,
                        capture_output=True
                    )
                except FileNotFoundError:
                    subprocess.run(
                        ["wget", "-O", str(self.model_path), self.model_url],
                        check=True,
                        capture_output=True
                    )

                self.logger.info("Model downloaded successfully.")

            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to download model: {e.stderr}")
                raise RuntimeError("Model download failed") from e
            except FileNotFoundError as e:
                self.logger.error(
                    "Neither curl nor wget found for downloading model")
                raise RuntimeError(
                    "No download tool available (curl/wget)") from e

    # Backward compatibility methods
    def remove_background(self, image_bytes: bytes) -> np.ndarray:
        """Backward compatible method."""
        return self.remove_background_optimized(image_bytes)
