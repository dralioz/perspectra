"""Background removal adapter for Perspectra library."""

import io
import logging
import os
import subprocess
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image
from rembg import remove

from ..core.config import PerspectraConfig


class BackgroundRemovalAdapter:
    """
    Adapter class to remove background from images using rembg and PIL.
    Provides detailed logging and error handling for each step.
    """

    def __init__(self, config: Optional[PerspectraConfig] = None):
        """
        Initialize the BackgroundRemovalAdapter.

        Args:
            config: Configuration object. If None, uses default settings.
        """
        self.config = config or PerspectraConfig()

        # Setup logging if enabled
        if self.config.enable_logging:
            self.logger = logging.getLogger(__name__)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(getattr(logging, self.config.log_level))
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        # Ensure models directory exists
        self.model_dir = Path("models")
        self.model_path = self.model_dir / self.config.model_filename

        if self.config.use_local_model:
            self._ensure_model_exists()

        self.logger.info("BackgroundRemovalAdapter initialized successfully.")

    def remove_background(self, image_bytes: bytes) -> np.ndarray:
        """
        Remove the background from the given image bytes.

        Args:
            image_bytes: The image data in bytes.

        Returns:
            The image as a numpy array with background removed.

        Raises:
            Exception: If background removal fails.
        """
        try:
            self.logger.info("Loading image from bytes.")
            loaded_image = self._load_image_from_bytes(image_bytes)
            self.logger.info("Image loaded successfully. Removing background.")
            data = self._process_background_removal(loaded_image)
            self.logger.info("Background removed successfully.")
            return data
        except Exception as e:
            self.logger.error(
                "Error in remove_background: %s", e, exc_info=True)
            raise

    def _load_image_from_bytes(self, image_bytes: bytes) -> Image.Image:
        """
        Load an image from bytes using PIL.

        Args:
            image_bytes: The image data in bytes.

        Returns:
            The loaded PIL Image object.
        """
        try:
            self.logger.debug("Opening image from bytes using PIL.")
            input_image = Image.open(io.BytesIO(image_bytes))
            self.logger.debug("Image opened successfully.")
            return input_image
        except Exception as e:
            self.logger.error(
                "Error loading image with PIL: %s", e, exc_info=True)
            raise

    def _ensure_model_exists(self):
        """
        Check if the model exists in the specified path and filename, download if not.
        """
        # Check if models directory exists
        if not self.model_dir.exists():
            self.logger.info("Models directory not found. Creating...")
            self.model_dir.mkdir(parents=True, exist_ok=True)

        # Check if model file exists
        if not self.model_path.exists():
            try:
                self.logger.info("Downloading model from %s",
                                 self.config.model_url)
                # Try curl first (macOS/Linux), then wget as fallback
                try:
                    subprocess.run(
                        ["curl", "-L", "-o",
                            str(self.model_path), self.config.model_url],
                        check=True,
                        capture_output=True
                    )
                except FileNotFoundError:
                    # Fallback to wget if curl is not available
                    subprocess.run(
                        ["wget", "-O", str(self.model_path),
                         self.config.model_url],
                        check=True,
                        capture_output=True
                    )
                self.logger.info("Model downloaded successfully.")
            except subprocess.CalledProcessError as e:
                self.logger.error("Failed to download model: %s", e.stderr)
                raise RuntimeError("Model download failed") from e
            except FileNotFoundError as e:
                self.logger.error(
                    "Neither curl nor wget found for downloading model")
                raise RuntimeError(
                    "No download tool available (curl/wget)") from e

    def _process_background_removal(self, image: Image.Image) -> np.ndarray:
        """
        Remove the background from a PIL Image and return a numpy array.

        Args:
            image: The PIL Image object.

        Returns:
            The image as a numpy array with background removed.
        """
        try:
            self.logger.info("Extracting EXIF and ICC profile from image.")
            exif = image.info.get("exif")
            icc = image.info.get("icc_profile")

            # Configure model path if using local model
            if self.config.use_local_model:
                os.environ["U2NET_HOME"] = str(self.model_dir)

            with io.BytesIO() as buffer:
                self.logger.info("Saving image to buffer in BMP format.")
                image.save(buffer, format="BMP", exif=exif, icc_profile=icc)
                self.logger.info("Removing background using rembg.")
                output_image = remove(
                    buffer.getvalue(), only_mask=self.config.is_only_mask)

            self.logger.info("Opening processed image and converting to RGB.")
            image_rgb = Image.open(io.BytesIO(output_image)).convert("RGB")
            data = np.array(image_rgb)
            self.logger.info("Image converted to numpy array successfully.")
            return data
        except Exception as e:
            self.logger.error(
                "Error removing background: %s", e, exc_info=True)
            raise
