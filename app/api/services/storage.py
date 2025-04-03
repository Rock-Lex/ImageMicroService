import os
from app.core.config import UPLOAD_DIR
from app.api.utils.filename_utils import generate_unique_filename

def save_image(image_bytes: bytes, filename_with_extension: str = None) -> str:
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    if not filename_with_extension:
        filename, filename_with_extension = generate_unique_filename()

    file_path = os.path.join(UPLOAD_DIR, filename_with_extension)

    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path