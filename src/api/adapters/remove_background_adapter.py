"""Provide to remove background from images."""

import io
import logging
import os
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image
from rembg import remove

from src.core.config import load_settings


class BackgroundRemoveAdapter:
    """
    Adapter class to remove background from images using rembg and PIL.
    Provides detailed logging and error handling for each step.
    """

    def __init__(self):
        """
        Initializes the BackgroundRemoveAdapter and sets up the logger.
        Ensures the model is available locally.
        """
        self.logger = logging.getLogger()
        self.settings = load_settings()
        self.logger.info("BackgroundRemoveAdapter initializing...")

        # Ensure models directory exists
        self.model_dir = Path("models")
        self.model_path = self.model_dir / self.settings.MODEL_FILENAME

        if self.settings.USE_LOCAL_MODEL:
            self._ensure_model_exists()

        self.logger.info("BackgroundRemoveAdapter initialized successfully.")

    def __call__(self, image_bytes: bytes) -> np.ndarray:
        """
        Removes the background from the given image bytes.

        Args:
            image_bytes (bytes): The image data in bytes.

        Returns:
            np.ndarray: The image as a numpy array with background removed.
        """
        try:
            self.logger.info("Calling reload_with_pil to load image from bytes.")
            loaded_image = self.reload_with_pil(image_bytes)
            self.logger.info("Image loaded successfully. " "Proceeding to remove background.")
            data = self.remove_background(loaded_image)
            self.logger.info("Background removed successfully.")
            return data
        except Exception as e:
            self.logger.error("Error in __call__: %s", e, exc_info=True)
            raise

    def reload_with_pil(self, image_bytes: bytes) -> Image.Image:
        """
        Loads an image from bytes using PIL.

        Args:
            image_bytes (bytes): The image data in bytes.

        Returns:
            Image.Image: The loaded PIL Image object.
        """
        try:
            self.logger.debug("Opening image from bytes using PIL.")
            input_image = Image.open(io.BytesIO(image_bytes))
            self.logger.debug("Image opened successfully.")
            return input_image
        except Exception as e:
            self.logger.error("Error loading image with PIL: %s", e, exc_info=True)
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
                # Using wget command for downloading
                subprocess.run(
                    ["wget", "-O", str(self.model_path), self.settings.MODEL_URL], check=True, capture_output=True
                )
                self.logger.info("Model downloaded successfully.")
            except subprocess.CalledProcessError as e:
                self.logger.error("Failed to download model: %s", e.stderr)
                raise RuntimeError("Model download failed") from e

    def remove_background(self, image: Image.Image) -> np.ndarray:
        """
        Removes the background from a PIL Image and returns a numpy array.

        Args:
            image (Image.Image): The PIL Image object.

        Returns:
            np.ndarray: The image as a numpy array with background removed.
        """
        try:
            self.logger.info("Extracting EXIF and ICC profile from image.")
            exif = image.info.get("exif")
            icc = image.info.get("icc_profile")

            # Configure model path if using local model
            if self.settings.USE_LOCAL_MODEL:
                os.environ["U2NET_HOME"] = str(self.model_dir)

            with io.BytesIO() as buffer:
                self.logger.info("Saving image to buffer in BMP format.")
                image.save(buffer, format="BMP", exif=exif, icc_profile=icc)
                self.logger.info("Removing background using rembg.")
                output_image = remove(buffer.getvalue(), only_mask=self.settings.IS_ONLY_MASK)
            self.logger.info("Opening processed image and converting to RGB.")
            image_rgb = Image.open(io.BytesIO(output_image)).convert("RGB")
            data = np.array(image_rgb)
            self.logger.info("Image converted to numpy array successfully.")
            return data
        except Exception as e:
            self.logger.error("Error removing background: %s", e, exc_info=True)
            raise
