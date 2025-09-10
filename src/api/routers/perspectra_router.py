"""Perspectra Router Module."""

from fastapi import APIRouter, Depends, File, Form, UploadFile

from src.api.services.perspectra_service import PerspectraAdapterService
from src.models.requests import PerspectraRequestModel
from src.models.responses import PerspectraResponseModel

router = APIRouter(prefix="/perspectra", tags=["perspectra"])


@router.post("/removing-background", response_model=PerspectraResponseModel)
async def process_image(
    session_id: str = Form(...),
    guid: str = Form(...),
    channel_id: str = Form(...),
    image: UploadFile = File(...),
    service: PerspectraAdapterService = Depends(PerspectraAdapterService),
):
    """
    Endpoint to process an image using PerspectraAdapterService.
    """
    image_bytes = await image.read()
    request_model = PerspectraRequestModel(session_id=session_id, guid=guid, channel_id=channel_id, image=image_bytes)
    response = service(request_model)
    return response
