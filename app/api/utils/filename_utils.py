import uuid
import os
from app.core.config import UPLOAD_DIR, logger, IMAGE_FORMAT


def generate_unique_filename() -> [str, str]:
    filename = f"{uuid.uuid4().hex}"
    filename_with_extension = f"{filename}.{IMAGE_FORMAT.lower()}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return generate_unique_filename()
    return filename, filename_with_extension