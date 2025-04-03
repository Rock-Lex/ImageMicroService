# Image Microservice

This is an asynchronous image processing microservice built with FastAPI. It handles image uploads, converts images to WebP format, and compresses them using Pillow. The app runs with Uvicorn and tracks upload status using Redis to prevent premature access to images still being processed.

## Features
- Asynchronous image uploads using FastAPI background tasks
- Image conversion to WebP format and compression with Pillow
- Upload status tracking in Redis
- Secure authentication using JWT (RS256)

## Installation

### Prerequisites
- Python 3.9+
- Redis
- Uvicorn

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/image-microservice.git
   cd image-microservice
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   Create a `.env` file in the root directory and define:
   ```env
   UPLOAD_DIR=/var/www/uploads
   REDIS_URL=redis://localhost:6379/0
   JWT_ALGORITHM=RS256
   PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
   -----END PUBLIC KEY-----"
   ```

## Running the Service

Start the application with Uvicorn on localhost:
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### Upload Image
- **Endpoint:** `POST /upload`
- **Description:** Uploads an image for processing (conversion to WebP and compression).
- **Request:** Multipart form-data with an image file.
- **Response:** JSON with task ID and status.

### Download Processed Image
- **Endpoint:** `GET /{filename}`
- **Description:** Retrieves the processed WebP image. Checks the upload status in Redis (status code 202 if still being uploaded).

## Security
- JWT authentication with RS256 algorithm
- Public key stored in environment variables for token verification
