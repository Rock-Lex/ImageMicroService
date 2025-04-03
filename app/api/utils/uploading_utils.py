from app.core.config import logger
from app.api.services import image_processing, storage
from app.api.services.status_tracker import set_status


def process_and_store_image(file_bytes: bytes, filename: str):
    try:
        compressed_bytes = image_processing.compress_and_convert_image(file_bytes)
        storage.save_image(compressed_bytes, filename)
        set_status(filename, "complete")
    except Exception as e:
        logger.error(f"Error, while uploading image: {e}")
        set_status(filename, "failed")
