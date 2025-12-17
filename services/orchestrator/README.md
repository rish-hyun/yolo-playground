# Orchestrator Service

The Orchestrator Service acts as middleware between the Frontend and Vision services, coordinating inference requests and providing result annotation capabilities. It handles image processing, communicates with the Vision API, and overlays bounding boxes with labels on detection results.

## 🎯 Overview

This service:
- Receives image/video upload requests from the frontend
- Forwards requests to the Vision Service for inference
- Annotates detection results with colored bounding boxes and labels
- Provides health check proxying for the Vision Service
- Acts as an API gateway and coordination layer

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│      Orchestrator Service API               │
│           (FastAPI)                         │
├─────────────────────────────────────────────┤
│        API Routes (v1)                      │
│  /tasks/classify  /tasks/detect            │
│  /tasks/segment   /tasks/pose               │
│  /tasks/obb                                 │
├─────────────────────────────────────────────┤
│        Vision Client                        │
│  (HTTP client to Vision Service)           │
├─────────────────────────────────────────────┤
│        Annotator Module                     │
│  - Draw bounding boxes                      │
│  - Add labels with confidence               │
│  - Color management                         │
└─────────────────────────────────────────────┘
```

## 📁 Project Structure

```
orchestrator/
├── app/
│   ├── main.py                      # FastAPI application entry
│   ├── api/
│   │   └── v1/
│   │       ├── router.py            # Main API router
│   │       ├── tasks.py             # Task endpoint handlers
│   │       └── vision.py            # Vision service proxy routes
│   ├── client/
│   │   └── vision.py                # HTTP client for Vision API
│   └── annotator/
│       ├── annotator.py             # Image annotation logic
│       ├── color.py                 # Color palette and utilities
│       └── constants.py             # Annotation constants
├── Dockerfile                        # Container definition
├── .dockerignore                     # Docker build exclusions
└── requirements.txt                  # Python dependencies
```

## 🚀 Getting Started

### Using Docker (Recommended)

```bash
# From the orchestrator service directory
docker build -t orchestrator:latest .
docker run -p 9600:8000 \
  -e VISION_SERVICE_HOST=vision \
  -e VISION_SERVICE_PORT=8000 \
  orchestrator:latest
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install opencv-python  # Required for image processing

# Set environment variables
export VISION_SERVICE_HOST=localhost
export VISION_SERVICE_PORT=9500

# Run the service
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Access Points

- API Documentation: http://localhost:9600/docs
- Alternative Docs: http://localhost:9600/redoc
- Health Check: http://localhost:9600/health

## 📡 API Endpoints

### System Endpoints

#### Health Check
```http
GET /health
```
Returns orchestrator service health status.

**Response:**
```json
{
  "healthy": true,
  "message": "Orchestrator service is running"
}
```

#### Vision Service Health (Proxy)
```http
GET /api/v1/vision/health
```
Proxies health check to the Vision Service.

### Task Endpoints (v1)

All task endpoints accept image files and return annotated images as binary data.

#### 1. Object Detection
```http
POST /api/v1/tasks/detect
```
Detects objects and overlays annotated bounding boxes on the image.

**Status:** ✅ **Fully Implemented**

**Request:**
- Content-Type: `multipart/form-data`
- Field: `file` (image file: jpg, jpeg, png)

**Response:**
- Content-Type: `image/jpeg` or `image/png`
- Body: Binary image data with annotated bounding boxes

**Features:**
- Colored bounding boxes per class
- Class labels with confidence scores
- Automatic color assignment by class ID
- Smart text placement (above or below box)

#### 2. Classification
```http
POST /api/v1/tasks/classify
```
**Status:** 🚧 **Pending** (Returns original image without processing)

#### 3. Instance Segmentation
```http
POST /api/v1/tasks/segment
```
**Status:** 🚧 **Pending** (Returns original image without processing)

#### 4. Pose Estimation
```http
POST /api/v1/tasks/pose
```
**Status:** 🚧 **Pending** (Returns original image without processing)

#### 5. Oriented Bounding Boxes (OBB)
```http
POST /api/v1/tasks/obb
```
**Status:** 🚧 **Pending** (Returns original image without processing)

### Error Responses

```json
{
  "detail": "Video files will be supported in future."
}
```

**Status Codes:**
- `200` - Success
- `415` - Unsupported Media Type
- `422` - Validation Error
- `500` - Internal Server Error

## 🧩 Key Components

### 1. Annotator Class (`annotator/annotator.py`)

Handles drawing bounding boxes and labels on images using OpenCV.

**Key Features:**
- Adaptive line width based on image size
- High-quality anti-aliased rendering (LINE_AA)
- Smart text positioning (above/below boxes)
- Contrast-aware text colors (light/dark based on box color)

**Methods:**
```python
class Annotator:
    def __init__(self, image: np.ndarray) -> None:
        """Initialize with image and calculate optimal line widths"""
    
    def draw_box_label(
        self,
        class_id: int,
        label: str,
        confidence: float,
        bbox: tuple[int, int, int, int]
    ) -> None:
        """Draw bounding box with label on image"""
    
    def result(self) -> np.ndarray:
        """Return annotated image"""
```

**Drawing Logic:**
1. Select color based on class ID
2. Draw bounding box rectangle
3. Calculate text size
4. Draw filled background for text
5. Render text with confidence score
6. Handle edge cases (text near image borders)

### 2. Color Management (`annotator/color.py`)

Provides consistent color assignment and contrast utilities.

**Features:**
- Pre-defined color palette for different classes
- Deterministic color selection by class ID
- Luminance-based contrast calculation
- Light/dark text color selection

**Example:**
```python
color = Color.pick(class_id=5)  # Get consistent color for class 5
text_color = Color.dark() if color.is_light() else Color.light()
```

### 3. Vision Client (`client/vision.py`)

Async HTTP client for communicating with the Vision Service.

**Methods:**
```python
class VisionClient:
    async def detect(self, file: ImageFile) -> DetectionResponse:
        """Call Vision Service detection endpoint"""
    
    async def classify(self, file: ImageFile) -> ClassificationResponse:
        """Call Vision Service classification endpoint"""
    
    # Similar methods for segment, pose, obb
```

**Features:**
- Built on httpx for async HTTP requests
- Type-safe responses using Pydantic models
- Automatic JSON parsing and validation
- Connection pooling and timeout handling

### 4. Request Serialization (`api/v1/tasks.py`)

Dependency injection function for file upload handling.

```python
async def serialize(file: UploadFile) -> ImageFile:
    """Convert FastAPI UploadFile to ImageFile model"""
    - Validates content type (image vs video)
    - Reads file content into memory
    - Returns structured ImageFile object
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VISION_SERVICE_HOST` | Yes | `vision` | Hostname of Vision Service |
| `VISION_SERVICE_PORT` | Yes | `8000` | Port of Vision Service |

### Annotation Settings

Defined in the `Annotator` class:
```python
self._line_width = max(round(sum(image.shape[:2]) / 2 * 0.003), 2)
self._thickness = max(self._line_width - 1, 1)
self._font_scale = self._line_width / 3
self._font_face = cv2.FONT_HERSHEY_SIMPLEX
self._line_type = cv2.LINE_AA
```

## 🐳 Docker Configuration

### Base Image
```dockerfile
FROM python:3.13.2-slim
```

### System Dependencies
```bash
apt-get install -y --no-install-recommends \
    libgl1 \           # OpenGL for OpenCV
    libglib2.0-0       # GLib for OpenCV
```

### Build Context
```yaml
build:
  context: services/orchestrator
  additional_contexts:
    common: common  # Shared schemas and utilities
```

### Exposed Ports
- Internal: `8000` (Uvicorn server)
- External: `9600` (mapped in docker-compose)

## 📦 Dependencies

```
fastapi==0.123.5           # Web framework
uvicorn==0.38.0            # ASGI server
python-multipart==0.0.20   # File upload support
opencv-python==4.12.0.88   # Image processing
httpx==0.28.1              # Async HTTP client
```

## 🎨 Annotation Details

### Bounding Box Rendering

1. **Box Drawing:**
   - Thickness: Adaptive based on image size
   - Line type: Anti-aliased (LINE_AA)
   - Color: Class-specific from palette

2. **Label Rendering:**
   - Format: `{class_name} {confidence:.2f}`
   - Background: Filled rectangle in box color
   - Text color: Contrast-optimized (light/dark)
   - Position: Above box (or below if near top edge)

3. **Color Palette:**
   - Consistent colors per class ID
   - High-contrast combinations
   - Visually distinct for neighboring classes

### Example Annotated Output

```
┌────────────────────────────┐
│ person 0.92                │  ← Label with confidence
├────────────────────────────┤
│                            │
│    [Detected Object]       │
│                            │
└────────────────────────────┘
```

## 🧪 Testing

### Manual API Testing

```bash
# Health check
curl http://localhost:9600/health

# Object detection
curl -X POST "http://localhost:9600/api/v1/tasks/detect" \
  -F "file=@test_image.jpg" \
  -o annotated_result.jpg

# Test with Python
import requests
response = requests.post(
    'http://localhost:9600/api/v1/tasks/detect',
    files={'file': open('test.jpg', 'rb')}
)
with open('result.jpg', 'wb') as f:
    f.write(response.content)
```

### Integration Testing

```python
# Check Vision Service connectivity
import httpx
client = httpx.AsyncClient(base_url="http://vision:8000")
response = await client.get("/health")
assert response.status_code == 200
```

## 🚧 Pending Features & TODOs

### Critical
- [ ] Implement classification annotation (current: returns original image)
- [ ] Implement segmentation mask overlay
- [ ] Implement pose keypoint drawing
- [ ] Implement OBB (rotated box) drawing
- [ ] Add video file processing support

### Enhancements
- [ ] Add configurable annotation styles via API
- [ ] Support custom color palettes
- [ ] Add label visibility toggle
- [ ] Add confidence threshold filtering
- [ ] Support batch image processing
- [ ] Add annotation opacity control
- [ ] Implement result caching
- [ ] Add annotation presets (minimal, detailed, custom)

### Annotation Features
- [ ] Draw segmentation masks with transparency
- [ ] Add pose skeleton connections
- [ ] Support for rotated bounding boxes (OBB)
- [ ] Add class probability distribution display
- [ ] Show inference time on image
- [ ] Add legend with all detected classes
- [ ] Support for custom fonts
- [ ] Multi-language label support

### Optimization
- [ ] Cache Vision Service responses
- [ ] Implement connection pooling
- [ ] Add request rate limiting
- [ ] Optimize image conversion pipelines
- [ ] Add concurrent request handling

### Monitoring
- [ ] Add request/response logging
- [ ] Track Vision Service availability
- [ ] Log annotation processing times
- [ ] Add error reporting and alerting

## 🔍 Troubleshooting

### Vision Service Connection Issues
```bash
# Check if Vision Service is reachable
curl http://vision:8000/health

# Verify environment variables
echo $VISION_SERVICE_HOST
echo $VISION_SERVICE_PORT
```

### OpenCV Import Errors
Ensure system dependencies are installed:
```bash
apt-get install libgl1 libglib2.0-0
```

### Image Quality Issues
- Check original image resolution
- Verify line width calculations
- Ensure anti-aliasing is enabled (LINE_AA)

## 🤝 Integration with Other Services

### Frontend Service
The frontend calls this service via HTTP:
```python
img_bytes = orchestrator_client.detect(file=image_file)
st.image(img_bytes)  # Display in Streamlit
```

### Vision Service
This service calls Vision API and processes results:
```python
response = await vision_client.detect(file)
annotator = Annotator(img)
for box in response.results[0].boxes:
    annotator.draw_box_label(...)
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenCV Drawing Functions](https://docs.opencv.org/master/d6/d6e/group__imgproc__draw.html)
- [httpx Documentation](https://www.python-httpx.org/)

## 📝 Notes

- Only detection task has annotation implementation
- Classification, segmentation, pose, and OBB return unprocessed images
- Video processing is not yet supported
- The service requires OpenCV with GUI support disabled in Docker
- All images are processed in memory (no file system writes)
- Color palette is fixed but can be extended in `color.py`
