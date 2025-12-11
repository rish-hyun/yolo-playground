# Vision Service

The Vision Service is the core AI component of the YOLO Playground platform. It provides REST API endpoints for various computer vision tasks using YOLO (You Only Look Once) models.

## Features

- **Object Detection**: Detect objects in images with bounding boxes and confidence scores
- **Instance Segmentation**: Generate pixel-level masks for detected objects
- **Image Classification**: Classify images into predefined categories
- **Pose Estimation**: Detect human keypoints and poses
- **Oriented Bounding Boxes (OBB)**: Detect objects with rotated bounding boxes

## Supported Models

- YOLO11n (nano) variants optimized for different tasks
- ONNX runtime for fast inference
- Automatic model conversion from PyTorch to ONNX

## API Endpoints

### Health Check
- `GET /health` - Service health status

### Vision Tasks

All endpoints accept image files via multipart/form-data and return JSON responses with detection results and inference speed metrics.

- `POST /api/v1/detect` - Object detection
- `POST /api/v1/segment` - Instance segmentation
- `POST /api/v1/classify` - Image classification
- `POST /api/v1/pose` - Pose estimation
- `POST /api/v1/obb` - Oriented bounding box detection

### Request Format

```bash
curl -X POST "http://localhost:9500/api/v1/detect" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg"
```

### Response Format

```json
{
  "results": [
    {
      "boxes": [
        {
          "id": 0,
          "label": "person",
          "confidence": 0.85,
          "bbox": {
            "x1": 100,
            "y1": 50,
            "x2": 200,
            "y2": 150
          }
        }
      ]
    }
  ],
  "speed": {
    "preprocess": 0.012,
    "inference": 0.045,
    "postprocess": 0.008
  }
}
```

## Configuration

### Environment Variables

- `MODEL_VERSION`: YOLO model version (default: "yolo11n")

### Model Weights

Models are stored in the `weights/` directory:
- `yolo11n.onnx` - Object detection
- `yolo11n-seg.onnx` - Instance segmentation
- `yolo11n-cls.onnx` - Classification
- `yolo11n-pose.onnx` - Pose estimation
- `yolo11n-obb.onnx` - Oriented bounding boxes

## Dependencies

- `ultralytics`: YOLO model implementation
- `onnx` & `onnxruntime`: ONNX model support
- `fastapi`: Web framework
- `uvicorn`: ASGI server

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables (optional):
   ```bash
   export MODEL_VERSION="yolo11n"
   ```

3. Run the service:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 9500
   ```

4. Access API documentation at: http://localhost:9500/docs

## Docker

Build and run with Docker:

```bash
docker build -t vision-service .
docker run -p 9500:8000 -e MODEL_VERSION="yolo11n" vision-service
```

## Architecture

The service uses a modular architecture:

- `models/`: YOLO model wrappers and base classes
- `api/v1/`: FastAPI routers and endpoints
- `weights/`: Pre-trained model weights
- `main.py`: Application entry point

Models are loaded on startup and cached for performance. ONNX models are preferred for inference speed, with automatic conversion from PyTorch models if needed.