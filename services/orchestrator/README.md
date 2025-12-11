# Orchestrator Service

The Orchestrator Service acts as an API gateway and coordinator between client applications and the Vision Service. It handles image processing requests, calls the appropriate vision endpoints, applies annotations to images, and returns the results.

## Features

- **Request Coordination**: Routes vision requests to the appropriate backend services
- **Image Annotation**: Automatically annotates detection results on images with bounding boxes and labels
- **Unified API**: Provides a consistent interface for all vision tasks
- **Streaming Responses**: Returns annotated images directly in the response

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Vision Tasks with Annotation

All endpoints accept image uploads and return annotated images with detection results overlaid.

- `POST /api/v1/detect` - Object detection with bounding box annotation
- `POST /api/v1/segment` - Instance segmentation (planned)
- `POST /api/v1/classify` - Image classification (planned)
- `POST /api/v1/pose` - Pose estimation (planned)
- `POST /api/v1/obb` - Oriented bounding box detection (planned)

### Request Format

```bash
curl -X POST "http://localhost:9600/api/v1/detect" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg" \
     --output annotated.jpg
```

### Response

Returns the original image with detection results annotated:
- Bounding boxes around detected objects
- Class labels and confidence scores
- Color-coded annotations for different object classes

## Configuration

### Environment Variables

- `VISION_SERVICE_HOST`: Vision service hostname (default: "localhost")
- `VISION_SERVICE_PORT`: Vision service port (default: "9500")

## Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `httpx`: Async HTTP client for vision service communication
- `opencv-python`: Image processing and annotation
- `python-multipart`: File upload handling

## Architecture

### Components

- `client/`: HTTP client for communicating with vision service
- `annotator/`: Image annotation utilities using OpenCV
- `api/v1/`: FastAPI routers and request handlers
- `main.py`: Application entry point

### Workflow

1. Client uploads an image
2. Orchestrator validates the image
3. Forwards request to Vision Service
4. Receives detection results
5. Applies annotations to the original image
6. Returns annotated image as streaming response

## Running Locally

1. Ensure Vision Service is running on the configured host/port

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```bash
   export VISION_SERVICE_HOST="localhost"
   export VISION_SERVICE_PORT="9500"
   ```

4. Run the service:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 9600
   ```

5. Access API documentation at: http://localhost:9600/docs

## Docker

Build and run with Docker:

```bash
docker build -t orchestrator-service .
docker run -p 9600:8000 \
  -e VISION_SERVICE_HOST="vision" \
  -e VISION_SERVICE_PORT="8000" \
  orchestrator-service
```

## Annotation Details

The annotator uses:
- Color-coded bounding boxes for different classes
- Class labels with confidence scores
- Automatic text positioning to avoid overlap
- High-contrast text colors based on background