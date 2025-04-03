import io
from PIL import Image as PILImage
from pillow_heif import register_heif_opener
from app.core.config import IMAGE_FORMAT, IMAGE_QUALITY, IMAGE_SUPPORTED_FORMATS

register_heif_opener()  # Enable HEIC support


def compress_and_convert_image(image_bytes: bytes) -> bytes:
    """
    Compress and convert an image using Pillow (with HEIC support if installed).

    :param image_bytes: Original image bytes.
    :param quality: Compression quality (1-100 for WebP/AVIF, 1-95 for JPEG/PNG).
    :param format: Output format (JPEG, PNG, WEBP, AVIF, GIF, TIFF, BMP, HEIC).
    :return: Compressed image bytes.
    """
    if IMAGE_FORMAT not in IMAGE_SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {IMAGE_FORMAT}. Choose from {IMAGE_SUPPORTED_FORMATS}.")

    with io.BytesIO(image_bytes) as input_buffer:
        with PILImage.open(input_buffer) as img:
            if format in {"JPEG", "JPG"}:
                img = img.convert("RGB")  # No transparency in JPEG
            elif format in {"WEBP", "AVIF", "HEIC"}:
                if img.mode not in {"RGB", "RGBA"}:
                    img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
            elif format == "PNG":
                if img.mode not in {"RGB", "RGBA", "P"}:
                    img = img.convert("RGBA")
            elif format in {"TIFF", "BMP"}:
                if img.mode not in {"RGB", "RGBA"}:
                    img = img.convert("RGB")

            with io.BytesIO() as output_buffer:
                img.save(output_buffer, format=IMAGE_FORMAT, quality=IMAGE_QUALITY)
                return output_buffer.getvalue()
