"""Main processor for Perspectra library."""

import base64
import logging
import time
from typing import Optional, Tuple

import cv2
import numpy as np

from .config import PerspectraConfig
from ..adapters.background_removal import BackgroundRemovalAdapter
from ..adapters.perspective_correction import PerspectiveCorrectionAdapter


class PerspectraProcessor:
    """
    Main processor class that combines background removal and perspective correction.

    This class provides a unified interface for processing images by:
    1. Removing the background from the input image
    2. Detecting and correcting perspective distortion
    3. Returning the processed result
    """

    def __init__(self, config: Optional[PerspectraConfig] = None):
        """
        Initialize the PerspectraProcessor.

        Args:
            config: Configuration object. If None, uses default settings.
        """
        self.config = config or PerspectraConfig()

        # Setup logging
        if self.config.enable_logging:
            self.logger = logging.getLogger(__name__)
            if not self.logger.handlers:
                handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                self.logger.setLevel(getattr(logging, self.config.log_level))
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.disabled = True

        # Initialize adapters
        self.bg_remover = BackgroundRemovalAdapter(config)
        self.perspective_corrector = PerspectiveCorrectionAdapter(config)

        self.logger.info("PerspectraProcessor initialized successfully.")

    def process_image(self, image_bytes: bytes) -> Tuple[bool, str, Optional[np.ndarray], float]:
        """
        Process an image by removing background and correcting perspective.

        Args:
            image_bytes: Input image as bytes

        Returns:
            Tuple containing:
            - success: Boolean indicating if processing was successful
            - error_message: Error message if processing failed, empty string if successful
            - result_image: Processed image as numpy array, None if failed
            - duration: Processing time in seconds
        """
        start_time = time.time()

        try:
            self.logger.info("Starting image processing...")

            # Step 1: Remove background
            self.logger.info("Step 1: Removing background...")
            background_mask = self.bg_remover.remove_background(image_bytes)
            self.logger.info("Background removal completed successfully.")

            # Step 2: Correct perspective
            self.logger.info("Step 2: Correcting perspective...")
            transformed_image = self.perspective_corrector.correct_perspective(
                background_mask, image_bytes
            )
            self.logger.info("Perspective correction completed successfully.")

            duration = time.time() - start_time
            self.logger.info("Image processing completed in %.2f seconds.", duration)

            return True, "", transformed_image, duration

        except Exception as e:
            duration = time.time() - start_time
            error_message = str(e)
            self.logger.error("Error processing image: %s", error_message, exc_info=True)
            return False, error_message, None, duration

    def process_image_to_base64(self, image_bytes: bytes) -> Tuple[bool, str, str, float]:
        """
        Process an image and return the result as base64 encoded string.

        Args:
            image_bytes: Input image as bytes

        Returns:
            Tuple containing:
            - success: Boolean indicating if processing was successful
            - error_message: Error message if processing failed, empty string if successful
            - result_base64: Processed image as base64 string, empty string if failed
            - duration: Processing time in seconds
        """
        success, error_message, result_image, duration = self.process_image(image_bytes)

        if success and result_image is not None:
            try:
                # Convert numpy array to base64
                _, buffer = cv2.imencode(".png", result_image)
                image_base64 = base64.b64encode(buffer).decode("utf-8")
                return True, "", image_base64, duration
            except Exception as e:
                error_msg = f"Failed to encode image to base64: {str(e)}"
                self.logger.error(error_msg)
                return False, error_msg, "", duration

        return success, error_message, "", duration

    def process_image_from_file(self, image_path: str) -> Tuple[bool, str, Optional[np.ndarray], float]:
        """
        Process an image from file path.

        Args:
            image_path: Path to the input image file

        Returns:
            Tuple containing:
            - success: Boolean indicating if processing was successful
            - error_message: Error message if processing failed, empty string if successful
            - result_image: Processed image as numpy array, None if failed
            - duration: Processing time in seconds
        """
        try:
            with open(image_path, 'rb') as f:
                image_bytes = f.read()
            return self.process_image(image_bytes)
        except Exception as e:
            error_message = f"Failed to read image file: {str(e)}"
            self.logger.error(error_message)
            return False, error_message, None, 0.0

    def save_processed_image(self, image_path: str, output_path: str) -> Tuple[bool, str, float]:
        """
        Process an image from file and save the result to another file.

        Args:
            image_path: Path to the input image file
            output_path: Path where the processed image will be saved

        Returns:
            Tuple containing:
            - success: Boolean indicating if processing was successful
            - error_message: Error message if processing failed, empty string if successful
            - duration: Processing time in seconds
        """
        success, error_message, result_image, duration = self.process_image_from_file(image_path)

        if success and result_image is not None:
            try:
                cv2.imwrite(output_path, result_image)
                self.logger.info("Processed image saved to: %s", output_path)
                return True, "", duration
            except Exception as e:
                error_msg = f"Failed to save processed image: {str(e)}"
                self.logger.error(error_msg)
                return False, error_msg, duration

        return success, error_message, duration
