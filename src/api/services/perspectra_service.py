"""Perspectra Service Module."""

import base64
import logging
import time

import cv2
from fastapi import Depends

from src.api.adapters.perspective_adapter import PerspectiveAndContourAdapter
from src.api.adapters.remove_background_adapter import BackgroundRemoveAdapter
from src.models.requests import PerspectraRequestModel
from src.models.responses import PerspectraResponseModel


class PerspectraAdapterService:
    """Service to handle image processing using BackgroundRemoveAdapter."""

    def __init__(
        self,
        bg_remove_adapter: BackgroundRemoveAdapter = Depends(BackgroundRemoveAdapter),
        perspective_adapter: PerspectiveAndContourAdapter = Depends(PerspectiveAndContourAdapter),
    ):
        self.logger = logging.getLogger()
        self.bg_remove_adapter = bg_remove_adapter
        self.perspective_adapter = perspective_adapter

    def __call__(self, request: PerspectraRequestModel) -> PerspectraResponseModel:
        start_time = time.time()
        try:
            # First remove the background from the image
            # Detect the object and wrap it to top view.
            backgroud_mask = self.bg_remove_adapter(request.image)
            transformed_image = self.perspective_adapter(backgroud_mask, request.image)

            # Convert the numpy array to PNG format and then base64 encode
            _, buffer = cv2.imencode(".png", transformed_image)
            image_base64 = base64.b64encode(buffer).decode("utf-8")
            response = PerspectraResponseModel(
                is_background_removed=True,
                is_image_wrapped=True,
                error_message="",
                result=True,
                duration=time.time() - start_time,
                processed_image=image_base64,
            )

        except Exception as e:
            self.logger.error("Error processing request: %s", e, exc_info=True)
            response = PerspectraResponseModel(
                is_background_removed=False,
                is_image_wrapped=False,
                error_message=str(e),
                result=False,
                duration=time.time() - start_time,
                processed_image="",
            )
        return response
