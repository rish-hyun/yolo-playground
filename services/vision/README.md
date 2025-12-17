# Vision Service

The Vision Service is the core inference engine of YOLO Playground, responsible for running YOLO11 models and performing computer vision tasks. It provides a RESTful API for object detection, classification, segmentation, pose estimation, and oriented bounding box detection.

## 🎯 Overview

This service:
- Loads and manages YOLO11 models in ONNX format
- Processes image data using OpenCV and NumPy
- Returns structured prediction results via FastAPI endpoints
- Automatically converts PyTorch models to optimized ONNX format
- Supports multiple YOLO tasks through a unified interface

## 🏗️ Architecture

```
┌────────────────────────────────────────┐
│         Vision Service API             │
│            (FastAPI)                   │
├────────────────────────────────────────┤
│         API Routes (v1)                │
│  /classify /detect /segment           │
│  /pose     /obb                        │
├────────────────────────────────────────┤
│         Model Layer                    │
│  - ClassificationModel                 │
│  - DetectionModel                      │
│  - SegmentationModel                   │
│  - PoseModel                           │
│  - OBBModel                            │
├────────────────────────────────────────┤
│      ONNX Runtime + Ultralytics       │
└────────────────────────────────────────┘
```

## 📁 Project Structure

```
vision/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       └── tasks.py         # API route handlers for all tasks
│   ├── models/
│   │   ├── __init__.py          # Model instance exports
│   │   ├── base.py              # BaseYOLOModel class
│   │   └── models.py            # Task-specific model classes
│   └── weights/
│       ├── yolo11n.onnx         # Detection model
│       ├── yolo11n-seg.onnx     # Segmentation model
│       ├── yolo11n-cls.onnx     # Classification model
│       ├── yolo11n-pose.onnx    # Pose estimation model
│       └── yolo11n-obb.onnx     # OBB detection model
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
└── requirements.docker.txt       # Docker-optimized dependencies
```

## 🚀 Getting Started

### Using Docker (Recommended)

```bash
# From the vision service directory
docker build -t vision:latest .
docker run -p 9500:8000 -e MODEL_VERSION=yolo11n vision:latest
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the service
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access Points

- API Documentation: http://localhost:9500/docs
- Alternative Docs: http://localhost:9500/redoc
- Health Check: http://localhost:9500/health

## 📡 API Endpoints

### System Endpoints

#### Health Check
```http
GET /health
```
Returns service health status.

**Response:**
```json
{
  "healthy": true,
  "message": "Vision service is running"
}
```

### Task Endpoints (v1)

#### 1. Object Detection
```http
POST /api/v1/detect
```
Detect objects in an image and return bounding boxes with class labels.

**Status:** ✅ **Implemented**

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file: jpg, jpeg, png)

**Response:**
```json
{
  "results": [
    {
      "boxes": [
        {
          "id": 0,
          "label": "person",
          "confidence": 0.92,
          "bbox": {
            "x1": 100.0,
            "y1": 150.0,
            "x2": 300.0,
            "y2": 450.0
          }
        }
      ]
    }
  ],
  "speed": {
    "preprocess": 2.3,
    "inference": 45.6,
    "postprocess": 1.2
  }
}
```

#### 2. Classification
```http
POST /api/v1/classify
```
Classify the entire image into predefined categories.

**Status:** 🚧 **Pending Implementation** (Currently returns empty results)

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file: jpg, jpeg, png)

**Response:**
```json
{
  "results": [],
  "speed": {
    "preprocess": 0.0,
    "inference": 0.0,
    "postprocess": 0.0
  }
}
```

#### 3. Instance Segmentation
```http
POST /api/v1/segment
```
Perform instance segmentation with pixel-level masks.

**Status:** 🚧 **Pending Implementation** (Currently returns empty results)

#### 4. Pose Estimation
```http
POST /api/v1/pose
```
Detect human poses and keypoints.

**Status:** 🚧 **Pending Implementation** (Currently returns empty results)

#### 5. Oriented Bounding Boxes (OBB)
```http
POST /api/v1/obb
```
Detect objects with rotated bounding boxes.

**Status:** 🚧 **Pending Implementation** (Currently returns empty results)

### Error Responses

```json
{
  "detail": "Unsupported file type."
}
```

**Status Codes:**
- `200` - Success
- `415` - Unsupported Media Type (e.g., video files not yet supported)
- `422` - Validation Error
- `500` - Internal Server Error

## 🧩 Key Components

### 1. BaseYOLOModel (`models/base.py`)

Abstract base class for all YOLO models with automatic ONNX conversion.

**Features:**
- Loads PyTorch models and converts to ONNX format
- Caches ONNX models in `weights/` directory
- Handles dynamic input shapes
- Provides unified inference interface

**Key Methods:**
```python
class BaseYOLOModel:
    task: ClassVar[Task]
    
    @classmethod
    def load(cls, model_version: ModelVersion) -> YOLO:
        """Load or convert model to ONNX format"""
        
    def __call__(self, images: List[np.ndarray]) -> Iterable[Results]:
        """Run inference on images"""
```

### 2. Task-Specific Models (`models/models.py`)

Specialized model classes for each YOLO task:
- `ClassificationModel`
- `DetectionModel`
- `SegmentationModel`
- `PoseModel`
- `OBBModel`

### 3. API Route Handlers (`api/v1/tasks.py`)

FastAPI route handlers that:
1. Accept file uploads via `multipart/form-data`
2. Deserialize images using OpenCV
3. Run model inference
4. Return structured JSON responses

**Key Function:**
```python
async def serialize(file: UploadFile) -> List[np.ndarray]:
    """Convert uploaded file to OpenCV image array"""
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_VERSION` | `yolo11n` | YOLO model version (n/s/m/l/x) |

### Supported Model Versions

| Version | Size | Speed | Accuracy |
|---------|------|-------|----------|
| `yolo11n` | ~6MB | Fastest | Baseline |
| `yolo11s` | ~25MB | Fast | Good |
| `yolo11m` | ~50MB | Medium | Better |
| `yolo11l` | ~100MB | Slow | High |
| `yolo11x` | ~150MB | Slowest | Highest |

### Model File Naming Convention

Models follow the pattern: `{version}{suffix}.onnx`
- Detection: `yolo11n.onnx`
- Segmentation: `yolo11n-seg.onnx`
- Classification: `yolo11n-cls.onnx`
- Pose: `yolo11n-pose.onnx`
- OBB: `yolo11n-obb.onnx`

## 🐳 Docker Configuration

### Base Image
Uses `ultralytics/ultralytics:8.3.236-python` which includes:
- Python 3.x
- Pre-installed Ultralytics YOLO
- Optimized for inference

### Build Context
The Dockerfile uses multi-context builds:
```yaml
build:
  context: services/vision
  additional_contexts:
    common: common  # Shared schemas and utilities
```

### Exposed Ports
- Internal: `8000` (Uvicorn server)
- External: `9500` (mapped in docker-compose)

## 📦 Dependencies

### Runtime Dependencies
```
ultralytics==8.3.233      # YOLO model implementation
onnx==1.19.1              # ONNX format support
onnxruntime==1.23.2       # ONNX inference engine
onnxslim==0.1.78          # Model optimization
fastapi==0.123.5          # Web framework
uvicorn==0.38.0           # ASGI server
python-multipart==0.0.20  # File upload support
```

### Image Processing
- OpenCV (opencv-python) - via Ultralytics base image
- NumPy - via Ultralytics base image

## 🧪 Testing

### Manual API Testing

```bash
# Health check
curl http://localhost:9500/health

# Object detection
curl -X POST "http://localhost:9500/api/v1/detect" \
  -F "file=@test_image.jpg" \
  -H "accept: application/json"

# Test with Python
python -c "
import requests
response = requests.post(
    'http://localhost:9500/api/v1/detect',
    files={'file': open('test.jpg', 'rb')}
)
print(response.json())
"
```

### Interactive Testing

Visit http://localhost:9500/docs for Swagger UI with built-in testing interface.

## 🚧 Pending Features & TODOs

### Critical
- [ ] Implement classification task (model inference commented out)
- [ ] Implement segmentation task (model inference commented out)
- [ ] Implement pose estimation task (model inference commented out)
- [ ] Implement OBB task (model inference commented out)
- [ ] Add video file support (currently returns 415 error)

### Enhancements
- [ ] Add batch processing support for multiple images
- [ ] Implement model warm-up on startup
- [ ] Add model caching/pre-loading
- [ ] Support for custom confidence thresholds
- [ ] Support for custom NMS thresholds
- [ ] Add result filtering options
- [ ] Implement GPU acceleration support
- [ ] Add model benchmarking endpoint
- [ ] Support for custom trained models
- [ ] Implement streaming inference for videos

### Optimization
- [ ] Profile and optimize inference speed
- [ ] Implement model quantization
- [ ] Add result caching for identical requests
- [ ] Memory usage optimization
- [ ] Support for TensorRT backend

### Monitoring
- [ ] Add inference metrics endpoint
- [ ] Log inference times and throughput
- [ ] Add error tracking and reporting
- [ ] Implement rate limiting

## 🔍 Troubleshooting

### Model Not Found
If you see model loading errors:
1. Ensure the `weights/` directory contains ONNX models
2. Check `MODEL_VERSION` environment variable is correct
3. First run will auto-convert .pt to .onnx (may take time)

### Memory Issues
- Use smaller model versions (yolo11n, yolo11s)
- Reduce image resolution before sending
- Enable swap memory in Docker settings

### Slow Inference
- Use GPU-enabled Docker image
- Switch to smaller model variant
- Check if ONNX Runtime is using CPU optimizations

## 🤝 Integration with Other Services

### Orchestrator Service
The orchestrator service calls this API via HTTP:
```python
response = await vision_client.detect(file)
# Returns: DetectionResponse with boxes and speed metrics
```

### Expected Response Format
All endpoints return responses conforming to Pydantic models in `common/schemas/responses.py`.

## 📚 Additional Resources

- [Ultralytics YOLO Documentation](https://docs.ultralytics.com/)
- [ONNX Runtime Documentation](https://onnxruntime.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📝 Notes

- Video processing is partially implemented but returns 415 errors
- Classification, segmentation, pose, and OBB endpoints are stubs
- Only detection task is fully functional
- Models are automatically converted to ONNX on first run
- ONNX models provide ~2-3x inference speedup vs PyTorch
