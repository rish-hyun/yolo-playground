# Frontend Service

The Frontend Service provides an interactive web-based user interface built with Streamlit for the YOLO Playground application. It allows users to upload images, select inference modes and tasks, and visualize annotated results in real-time.

## 🎯 Overview

This service:
- Provides a responsive web UI using Streamlit
- Allows image/video/webcam mode selection
- Supports all YOLO task types (detect, classify, segment, pose, obb)
- Performs health checks on backend services
- Displays input images alongside annotated results
- Communicates with the Orchestrator Service via HTTP

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Streamlit Web Application           │
│         (Frontend UI)                   │
├─────────────────────────────────────────┤
│          User Interface                 │
│  - Mode selector (Image/Video/Webcam)  │
│  - Task selector (5 YOLO tasks)        │
│  - File uploader                        │
│  - Result display (side-by-side)       │
├─────────────────────────────────────────┤
│     Orchestrator Client                 │
│  (HTTP client using requests)          │
└─────────────────────────────────────────┘
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── main.py                  # Streamlit application entry point
│   └── client/
│       ├── __init__.py          # Client instance export
│       └── orchestrator.py      # HTTP client for Orchestrator API
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Getting Started

### Using Docker (Recommended)

```bash
# From the frontend service directory
docker build -t frontend:latest .
docker run -p 9700:8000 \
  -e ORCHESTRATOR_SERVICE_HOST=orchestrator \
  -e ORCHESTRATOR_SERVICE_PORT=8000 \
  frontend:latest
```

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ORCHESTRATOR_SERVICE_HOST=localhost
export ORCHESTRATOR_SERVICE_PORT=9600

# Run the service
cd app
streamlit run main.py --server.port=8000 --server.address=0.0.0.0
```

### Access Points

- Web UI: http://localhost:9700
- Streamlit runs on port 8000 internally (mapped to 9700 externally)

## 🖥️ User Interface

### Layout

```
┌─────────────────────────────────────────────────────────┐
│                   YOLO Playground                        │
├──────────────┬──────────────────────────────────────────┤
│   Sidebar    │           Main Content Area              │
│              │                                           │
│  Mode:       │    ┌──────────┐   ┌──────────┐          │
│  ○ Image     │    │  Input   │   │  Result  │          │
│  ○ Video     │    │  Image   │   │  Image   │          │
│  ○ Webcam    │    └──────────┘   └──────────┘          │
│              │                                           │
│  Task:       │    [File Uploader]                       │
│  ○ Detect    │                                           │
│  ○ Classify  │    [Inference Status]                    │
│  ○ Segment   │                                           │
│  ○ Pose      │                                           │
│  ○ OBB       │                                           │
└──────────────┴──────────────────────────────────────────┘
```

### Features

#### 1. Service Health Check
On first load, the UI performs comprehensive health checks:
```
✓ Checking services availability...
  ✓ Orchestrator service is healthy!
  ✓ Vision service is healthy!
✓ All services are healthy!
```

**Retry Logic:**
- 5 attempts per service
- 2-second delay between attempts
- Graceful error handling with user feedback

#### 2. Mode Selection
Three inference modes available:

| Mode | Status | Description |
|------|--------|-------------|
| **Image** | ✅ Working | Upload and process single images |
| **Video** | 🚧 Pending | Process video files frame-by-frame |
| **Webcam** | 🚧 Pending | Real-time inference from webcam feed |

#### 3. Task Selection
Five YOLO tasks available:

| Task | Status | Description |
|------|--------|-------------|
| **Detect** | ✅ Working | Object detection with bounding boxes |
| **Classify** | 🚧 Pending | Image classification |
| **Segment** | 🚧 Pending | Instance segmentation |
| **Pose** | 🚧 Pending | Human pose estimation |
| **OBB** | 🚧 Pending | Oriented bounding box detection |

#### 4. Image Mode (Implemented)
- File uploader accepts: `.png`, `.jpg`, `.jpeg`
- Side-by-side display of input and result
- Automatic inference on upload
- Loading spinner during processing

#### 5. Video Mode (Placeholder)
```python
# Currently shows info message
st.info("Video mode is not yet implemented.")
```

#### 6. Webcam Mode (Placeholder)
```python
# streamlit-webrtc integration commented out
st.info("Webcam mode is not yet implemented.")
```

## 🧩 Key Components

### 1. Main Application (`main.py`)

**Entry Point:**
```python
def main():
    st.set_page_config(
        page_title="YOLO Playground",
        page_icon="🤖",
        layout="wide",
    )
```

**Custom Styling:**
```css
.stMainBlockContainer {
    padding-left: 5rem;
    padding-right: 5rem;
}
button[data-baseweb="tab"] {
    font-size: 24px;
}
```

**State Management:**
```python
st.session_state.setdefault("services_health_checked", False)
```

### 2. Health Check Logic

**Orchestrator Health:**
```python
def _is_orchestrator_healthy(attempts: int = 5, delay: int = 2) -> bool:
    for _ in range(attempts):
        healthy = orchestrator_client.is_orchestrator_healthy()
        if healthy:
            return True
        time.sleep(delay)
    return False
```

**Vision Service Health (via Orchestrator):**
```python
def _is_vision_healthy(attempts: int = 5, delay: int = 2) -> bool:
    for _ in range(attempts):
        healthy = orchestrator_client.is_vision_healthy()
        if healthy:
            return True
        time.sleep(delay)
    return False
```

### 3. Image Processing Workflow

```python
def image_mode(task: str):
    # 1. File upload
    image_file = st.file_uploader(
        label="Upload an image file",
        type=["png", "jpg", "jpeg"],
    )
    
    # 2. Display input and output side-by-side
    _input, _output = st.columns(2)
    
    # 3. Create ImageFile object
    image_file = ImageFile(
        file_name=image_file.name,
        file_content=image_file.read(),
        content_type=image_file.type,
    )
    
    # 4. Call orchestrator service
    img_bytes = getattr(orchestrator_client, task)(file=image_file)
    
    # 5. Display result
    st.image(img_bytes)
```

### 4. Orchestrator Client (`client/orchestrator.py`)

**Client Initialization:**
```python
class OrchestratorClient:
    def __init__(self, host: str, port: int):
        self._base_url = f"http://{host}:{port}"
        self._client = requests.Session()
```

**Health Check Methods:**
```python
def is_orchestrator_healthy(self) -> bool:
    """Check orchestrator service health"""
    
def is_vision_healthy(self) -> bool:
    """Check vision service health via orchestrator"""
```

**Task Methods:**
```python
def detect(self, file: ImageFile) -> bytes:
    """Call detection endpoint and return annotated image"""
    
# Similar methods for: classify, segment, pose, obb
```

**Request Handler:**
```python
def request(
    self,
    method: HttpMethod,
    endpoint: str,
    file: Optional[ImageFile] = None,
) -> Any:
    response = self._client.request(
        method=method.value,
        url=f"{self._base_url}{endpoint}",
        files={"file": file} if file else None,
        timeout=10,
    )
    response.raise_for_status()
    return response.json() if file is None else response.content
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ORCHESTRATOR_SERVICE_HOST` | Yes | `orchestrator` | Orchestrator service hostname |
| `ORCHESTRATOR_SERVICE_PORT` | Yes | `8000` | Orchestrator service port |

### Streamlit Configuration

The service uses custom Streamlit settings:
```python
st.set_page_config(
    page_title="YOLO Playground",
    page_icon="🤖",
    layout="wide",  # Full-width layout
)
```

### Client Configuration

Hardcoded in `client/__init__.py`:
```python
orchestrator_client = OrchestratorClient(
    host=os.getenv("ORCHESTRATOR_SERVICE_HOST", "orchestrator"),
    port=int(os.getenv("ORCHESTRATOR_SERVICE_PORT", "8000")),
)
```

## 🐳 Docker Configuration

### Base Image
```dockerfile
FROM python:3.13.2-slim
```

### Build Context
```yaml
build:
  context: services/frontend
  additional_contexts:
    common: common  # Shared schemas
```

### Startup Command
```dockerfile
CMD ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]
```

### Exposed Ports
- Internal: `8000` (Streamlit server)
- External: `9700` (mapped in docker-compose)

## 📦 Dependencies

```
streamlit==1.52.1          # Web UI framework
opencv-python==4.12.0.88   # Image processing
httpx==0.28.1              # Alternative HTTP client (unused)
pydantic==2.12.5           # Data validation
```

### Commented Dependencies
```
# streamlit-webrtc==0.64.5  # For webcam mode (future)
```

## 🎨 UI Features

### Custom CSS Styling
- Wide layout with custom padding
- Enlarged tab buttons (24px font)
- Transparent app header
- Responsive design

### User Experience
- **Loading States**: Spinners during inference
- **Error Handling**: Clear error messages for service failures
- **Visual Feedback**: Status indicators for health checks
- **Side-by-side Comparison**: Input vs output images

### Streamlit Components Used
- `st.file_uploader()` - File upload
- `st.radio()` - Mode/task selection
- `st.image()` - Image display
- `st.columns()` - Layout
- `st.spinner()` - Loading indicator
- `st.status()` - Health check status
- `st.info()` - Placeholder messages

## 🧪 Testing

### Manual Testing

1. **Start the service:**
   ```bash
   streamlit run main.py
   ```

2. **Test health checks:**
   - Should see green checkmarks for both services
   - If failed, check orchestrator/vision connectivity

3. **Test image upload:**
   - Upload a `.jpg` or `.png` file
   - Should see original on left, result on right

4. **Test different tasks:**
   - Switch task in sidebar
   - Re-upload image
   - Currently only "detect" shows annotations

### Client Testing

```python
from client import orchestrator_client

# Test health
assert orchestrator_client.is_orchestrator_healthy()
assert orchestrator_client.is_vision_healthy()

# Test detection
from common.schemas.requests import ImageFile
img_file = ImageFile(
    file_name="test.jpg",
    file_content=open("test.jpg", "rb").read(),
    content_type="image/jpeg"
)
result = orchestrator_client.detect(file=img_file)
assert isinstance(result, bytes)
```

## 🚧 Pending Features & TODOs

### Critical
- [ ] Implement video file processing mode
- [ ] Implement webcam live inference mode
- [ ] Enable streamlit-webrtc for webcam support

### UI Enhancements
- [ ] Add confidence threshold slider
- [ ] Add NMS threshold slider
- [ ] Display inference speed metrics
- [ ] Show detected class statistics
- [ ] Add model version selector
- [ ] Add result download button
- [ ] Multi-image batch upload support
- [ ] Image gallery view for results
- [ ] Add zoom/pan for result images

### Video Mode Features
- [ ] Video file upload support
- [ ] Frame-by-frame processing
- [ ] Video playback with annotations
- [ ] Frame rate control
- [ ] Export annotated video
- [ ] Progress bar for video processing

### Webcam Mode Features
- [ ] Real-time webcam feed
- [ ] FPS display
- [ ] Record functionality
- [ ] Snapshot capture
- [ ] Performance optimization for real-time

### Configuration
- [ ] Settings page for advanced options
- [ ] Save/load inference presets
- [ ] User preferences persistence
- [ ] API endpoint configuration UI
- [ ] Theme customization

### Error Handling
- [ ] Better error messages for users
- [ ] Network error recovery
- [ ] Timeout configuration
- [ ] Retry logic with exponential backoff
- [ ] Service unavailable fallback UI

### Monitoring
- [ ] Request/response logging
- [ ] Performance metrics display
- [ ] Service status dashboard
- [ ] Usage statistics

## 🔍 Troubleshooting

### Service Health Check Fails
```python
# Check if orchestrator is reachable
curl http://orchestrator:8000/health

# Verify environment variables
import os
print(os.getenv("ORCHESTRATOR_SERVICE_HOST"))
print(os.getenv("ORCHESTRATOR_SERVICE_PORT"))
```

### File Upload Not Working
- Check file size limits (Streamlit default: 200MB)
- Verify file format (png, jpg, jpeg only)
- Check browser console for errors

### Images Not Displaying
- Verify image bytes are valid
- Check content-type header from orchestrator
- Try refreshing the page

### Webcam Mode Commented Out
```python
# Uncomment in requirements.txt:
streamlit-webrtc==0.64.5

# Uncomment in main.py:
from streamlit_webrtc import webrtc_streamer
```

## 🤝 Integration with Other Services

### Orchestrator Service
The frontend communicates exclusively with the orchestrator:

```python
# Health checks
orchestrator_client.is_orchestrator_healthy()
orchestrator_client.is_vision_healthy()  # Proxied through orchestrator

# Inference
img_bytes = orchestrator_client.detect(file=image_file)
```

**Response Format:**
- Returns binary image data (bytes)
- Already annotated by orchestrator
- Ready for display via `st.image()`

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit WebRTC](https://github.com/whitphx/streamlit-webrtc)
- [Requests Library](https://requests.readthedocs.io/)

## 📝 Notes

- Only image mode is fully functional
- Video and webcam modes are placeholders
- Only detection task shows meaningful results
- Classification, segmentation, pose, and OBB return unmodified images
- Health checks run only once per session (cached in session_state)
- The UI uses session state for health check caching
- Custom CSS is injected via `st.markdown()` with `unsafe_allow_html=True`
- File upload is synchronous (blocks until complete)
- No file size validation implemented yet
- streamlit-webrtc is commented out in requirements (future dependency)

## 🎯 Design Decisions

1. **Session State for Health Checks**: Avoids repeated checks on every rerun
2. **Synchronous HTTP Client**: Uses `requests` instead of `httpx` for simplicity
3. **Side-by-side Display**: Two columns for input/output comparison
4. **Wide Layout**: Maximizes screen real estate for images
5. **Placeholder Messages**: Clear communication for unimplemented features
