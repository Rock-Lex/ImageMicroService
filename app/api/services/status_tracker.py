from app.core.redis_client import redis_client


def set_status(filename: str, status: str, expire: int = 3600):
    """
    Set the processing status for an image.

    :param filename: Unique filename for the image.
    :param status: A string representing status ("processing", "complete", "failed").
    :param expire: Time in seconds after which the status expires (default 1 hour).
    """
    redis_client.set(f"image_status:{filename}", status, ex=expire)


def get_status(filename: str):
    """
    Retrieve the processing status for an image.

    :param filename: Unique filename for the image.
    :return: Status string or None if not found.
    """
    return redis_client.get(f"image_status:{filename}")
