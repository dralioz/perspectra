# pylint: disable=no-member
import logging
import os
from datetime import datetime

import cv2
import numpy as np

from src.core.config import load_settings


class PerspectiveAndContourAdapter:
    """
    Maskedeki beyaz alanı bulup, dört köşesini tespit ederek
    yukarıdan bakış (top view) perspektifine dönüştüren adapter.
    """

    def __init__(self):
        """Initialize the adapter with a logger and settings."""
        self.logger = logging.getLogger(__name__)
        self.settings = load_settings()

    def find_contours(self, mask: np.ndarray) -> np.ndarray:
        """
        Find and return the largest contour in the mask.

        Args:
            mask (np.ndarray): Binary mask where white area is the region of interest

        Returns:
            np.ndarray: The largest contour found in the mask

        Raises:
            ValueError: If no contours are found in the mask
        """
        # Convert the image to the grayscale
        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # pylint: disable=no-member

        if not contours:
            raise ValueError("Maskede kontur bulunamadı.")

        largest_contour = max(contours, key=cv2.contourArea)  # pylint: disable=no-member

        # Save contours if enabled in config
        if self.settings.SAVE_CONTOURS:
            try:
                # Create debug directory if it doesn't exist
                debug_dir = os.path.join(self.settings.CONTOURS_PATH, datetime.now().strftime("%Y%m%d_%H%M%S"))
                os.makedirs(debug_dir, exist_ok=True)

                # Save the original mask with contours drawn
                debug_image = mask.copy()
                cv2.drawContours(debug_image, [largest_contour], -1, (0, 255, 0), 2)

                # Save both the original mask and the mask with contours
                cv2.imwrite(os.path.join(debug_dir, "original_mask.png"), mask)
                cv2.imwrite(os.path.join(debug_dir, "contours.png"), debug_image)

                self.logger.info("Contours saved to: %s", debug_dir)
            except Exception as e:
                self.logger.error("Failed to save contours: %s", str(e))

        return largest_contour

    def find_corners(self, contour: np.ndarray) -> np.ndarray:
        """
        Find four corners of the contour using improved approxPolyDP with multiple epsilon values.

        Args:
            contour (np.ndarray): The contour to find corners for

        Returns:
            np.ndarray: Array of four corner points
        """
        # Try different epsilon values to find the best 4-point approximation
        epsilons = [0.01, 0.02, 0.03, 0.05, 0.1]

        for epsilon_factor in epsilons:
            epsilon = epsilon_factor * cv2.arcLength(contour, True)  # pylint: disable=no-member
            approx = cv2.approxPolyDP(contour, epsilon, True)  # pylint: disable=no-member

            if len(approx) == 4:
                return approx.reshape(4, 2)
            elif len(approx) < 4:
                # If we get fewer than 4 points, this epsilon is too large
                break

        # If approxPolyDP doesn't work, use minAreaRect as fallback
        rect = cv2.minAreaRect(contour)  # pylint: disable=no-member
        box = cv2.boxPoints(rect)  # pylint: disable=no-member

        return box.astype(np.float32)

    def order_points(self, pts: np.ndarray) -> np.ndarray:
        """
        Order points as [top-left, top-right, bottom-right, bottom-left].

        Algorithm:
        1. Sort points by x coordinates (x0, x1, x2, x3)
        2. Sort points by y coordinates (y0, y1, y2, y3)
        3. Calculate angle between x0 and x1
        4. Assign corners based on angle sign

        Args:
            pts (np.ndarray): Array of 4 points to order

        Returns:
            np.ndarray: Ordered points as [top-left, top-right, bottom-right, bottom-left]
        """
        pts = pts.reshape(4, 2)

        # Sort points
        x_sorted = pts[np.argsort(pts[:, 0])]  # x0, x1, x2, x3
        y_sorted = pts[np.argsort(pts[:, 1])]  # y0, y1, y2, y3

        # Calculate angle between x0 and x1 (multiply by -1 for matrix coordinates)
        dx = x_sorted[1][0] - x_sorted[0][0]
        dy = x_sorted[1][1] - x_sorted[0][1]
        angle = np.degrees(np.arctan2(dy, dx)) * -1

        # Assign corners based on angle
        if angle >= 0:  # Positive angle
            BL = x_sorted[0]  # x0 (smallest x)
            TR = x_sorted[3]  # x3 (largest x)
            TL = y_sorted[0]  # y0 (smallest y)
            # BR = remaining point
            used_points = [BL, TR, TL]
            BR = None
            for point in pts:
                if not any(np.array_equal(point, used) for used in used_points):
                    BR = point
                    break
        else:  # Negative angle
            BL = y_sorted[3]  # y3 (largest y)
            TR = y_sorted[0]  # y0 (smallest y)
            TL = x_sorted[0]  # x0 (smallest x)
            # BR = remaining point
            used_points = [BL, TR, TL]
            BR = None
            for point in pts:
                if not any(np.array_equal(point, used) for used in used_points):
                    BR = point
                    break

        return np.array([TL, TR, BR, BL], dtype="float32")

    def perspective_transform(self, mask: np.ndarray, src_pts: np.ndarray) -> np.ndarray:
        """
        Apply perspective transform with 5% padding to prevent corner loss.

        Args:
            mask: Input image/mask to transform
            src_pts: Source points [TL, TR, BR, BL]

        Returns:
            Transformed image as perfect rectangle with padding
        """
        # Calculate edge lengths
        top_width = np.linalg.norm(src_pts[0] - src_pts[1])
        right_height = np.linalg.norm(src_pts[1] - src_pts[2])
        bottom_width = np.linalg.norm(src_pts[2] - src_pts[3])
        left_height = np.linalg.norm(src_pts[3] - src_pts[0])

        # Use average dimensions
        final_width = int((top_width + bottom_width) / 2)
        final_height = int((left_height + right_height) / 2)

        # Add 5% padding to prevent corner loss
        padding_factor = 0.05
        width_padding = int(final_width * padding_factor)
        height_padding = int(final_height * padding_factor)

        # Calculate padded dimensions
        padded_width = final_width + 2 * width_padding
        padded_height = final_height + 2 * height_padding

        # Define destination rectangle with padding
        dst_pts = np.array(
            [
                [width_padding, height_padding],  # top-left (with padding)
                [padded_width - width_padding - 1, height_padding],  # top-right
                [padded_width - width_padding - 1, padded_height - height_padding - 1],  # bottom-right
                [width_padding, padded_height - height_padding - 1],  # bottom-left
            ],
            dtype="float32",
        )

        self.logger.info(
            "Perspective transformation: %dx%d with 5%% padding (%dx%d)",
            final_width,
            final_height,
            padded_width,
            padded_height,
        )

        # Apply perspective transformation
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        result = cv2.warpPerspective(mask, M, (padded_width, padded_height))

        return result

    def find_contour_corners(self, mask: np.ndarray) -> np.ndarray:
        """
        Find ordered corner points of the largest contour in the mask.

        Args:
            mask (np.ndarray): Binary mask where white area is the region of interest

        Returns:
            np.ndarray: Ordered corner points in clockwise order starting from top-left

        Raises:
            ValueError: If no contours are found in the mask
        """
        try:
            contour = self.find_contours(mask)
            raw_corners = self.find_corners(contour)
            ordered_corners = self.order_points(raw_corners)

            self.logger.info("Found %d corner points", len(ordered_corners))

            return ordered_corners
        except Exception as e:
            self.logger.error("Error finding contour corners: %s", str(e))
            raise

    def __call__(self, mask: np.ndarray, bytes_image: bytes) -> np.ndarray:
        """
        Process mask to get top view perspective.

        Args:
            mask (np.ndarray): Binary mask where white area is the region of interest
            bytes_image (bytes): Original image bytes

        Returns:
            np.ndarray: Top view transformed original image

        Raises:
            ValueError: If no contours are found in the mask
            Exception: If perspective transformation fails
        """
        try:
            # Convert bytes to image
            original_image = self.convert_bytes_to_image(bytes_image)

            # Get dimensions
            mask_height, mask_width = mask.shape[:2]
            orig_height, orig_width = original_image.shape[:2]

            self.logger.info(
                "Processing image: mask=%dx%d, original=%dx%d", mask_width, mask_height, orig_width, orig_height
            )

            # Find corners in mask coordinates
            mask_corners = self.find_contour_corners(mask)

            # Scale corners to original image coordinates if dimensions differ
            if mask_width != orig_width or mask_height != orig_height:
                scale_x = orig_width / mask_width
                scale_y = orig_height / mask_height

                original_corners = mask_corners.copy()
                original_corners[:, 0] *= scale_x  # Scale x coordinates
                original_corners[:, 1] *= scale_y  # Scale y coordinates

                self.logger.info("Scaled corners for original image dimensions")
            else:
                original_corners = mask_corners

            # Apply perspective transform to original image
            transformed = self.perspective_transform(original_image, original_corners)
            self.logger.info("Successfully transformed perspective to top view")

            # Save debug images if enabled
            if self.settings.SAVE_TRANSFORMED:
                try:
                    debug_dir = os.path.join(self.settings.CONTOURS_PATH, datetime.now().strftime("%Y%m%d_%H%M%S"))
                    os.makedirs(debug_dir, exist_ok=True)

                    # Save transformed image
                    cv2.imwrite(os.path.join(debug_dir, "transformed.png"), transformed)

                    # Save original image with corners marked for debugging
                    debug_original = original_image.copy()
                    corner_labels = ["TL", "TR", "BR", "BL"]  # Top-Left, Top-Right, Bottom-Right, Bottom-Left
                    corner_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]  # Green, Red, Blue, Yellow

                    for i, corner in enumerate(original_corners.astype(int)):
                        # Draw circle for corner
                        cv2.circle(debug_original, tuple(corner), 15, corner_colors[i], -1)
                        # Add text label
                        cv2.putText(
                            debug_original,
                            f"{i}:{corner_labels[i]}",
                            tuple(corner + 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            corner_colors[i],
                            2,
                        )

                    cv2.imwrite(os.path.join(debug_dir, "original_with_corners.png"), debug_original)
                    self.logger.info("Debug images saved to: %s", debug_dir)
                except Exception as e:
                    self.logger.error("Error saving debug images: %s", str(e))

            return transformed
        except Exception as e:
            self.logger.error("Error in perspective transformation: %s", str(e))
            raise

    @staticmethod
    def convert_bytes_to_image(image_bytes: bytes) -> np.ndarray:
        """
        Convert byte array to OpenCV image.

        Args:
            image_bytes (bytes): Image in byte array format

        Returns:
            np.ndarray: Decoded OpenCV image
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
