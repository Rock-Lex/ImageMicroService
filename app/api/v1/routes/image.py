import os
import mimetypes
from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from app.api.utils.uploading_utils import process_and_store_image
from app.api.utils.filename_utils import generate_unique_filename
from app.api.models.image import ImageOut
from app.api.services.status_tracker import set_status, get_status
from app.core.security import verify_token
from app.core.config import UPLOAD_DIR, IMAGE_FORMAT

router = APIRouter()


@router.post("/upload", response_model=ImageOut)
async def upload_image(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        token: str = Depends(verify_token)
):
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")

    filename, filename_with_extension = generate_unique_filename()

    set_status(filename, "processing")

    background_tasks.add_task(process_and_store_image, file_bytes, filename_with_extension)

    return ImageOut(filename=filename)


@router.get("/{filename}")
async def get_image(filename: str):
    filename = filename + f".{IMAGE_FORMAT.lower()}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        status = get_status(filename)
        if status == "processing":
            return JSONResponse(
                status_code=202,
                content={"detail": "Image processing is in progress. Please try again shortly."}
            )
        elif status == "failed":
            raise HTTPException(status_code=500, detail="Image processing failed.")
        else:
            raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(file_path, media_type=mimetypes.guess_type(file_path)[0] or "application/octet-stream")


@router.delete("/{filename}")
async def delete_image(filename: str, token: str = Depends(verify_token)):
    filename_with_extension = filename + f".{IMAGE_FORMAT.lower()}"
    file_path = os.path.join(UPLOAD_DIR, filename_with_extension)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {e}")
    
    return JSONResponse(status_code=200, content={"detail": "Image deleted successfully"})


@router.put("/{filename}", response_model=ImageOut)
async def update_image(
    filename: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    token: str = Depends(verify_token)
):
    filename_with_extension = filename + f".{IMAGE_FORMAT.lower()}"
    file_path = os.path.join(UPLOAD_DIR, filename_with_extension)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {e}")
    
    set_status(filename, "processing")
    
    background_tasks.add_task(process_and_store_image, file_bytes, filename_with_extension)
    
    return ImageOut(filename=filename)