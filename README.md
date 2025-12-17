# YOLO Playground

A microservices-based computer vision application powered by YOLO11 models, featuring a Streamlit frontend, orchestration layer, and inference backend. This project demonstrates multiple YOLO tasks including object detection, classification, segmentation, pose estimation, and oriented bounding boxes.

## 🏗️ Architecture

The project follows a microservices architecture with three main services:

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │─────▶│ Orchestrator │─────▶│   Vision    │
│ (Streamlit) │      │   Service    │      │   Service   │
│  Port 9700  │      │  Port 9600   │      │  Port 9500  │
└─────────────┘      └──────────────┘      └─────────────┘
```

### Services

1. **Frontend** - Streamlit-based web UI for user interaction
2. **Orchestrator** - Middleware service that coordinates requests and annotates results
3. **Vision** - Core inference service running YOLO11 models

### Shared Components

- **common/** - Shared schemas, enums, and utilities
  - `schemas/` - Pydantic models for requests, responses, and results
  - `utils/` - Image conversion utilities (OpenCV ↔ bytes)

## 🚀 Features

### Supported YOLO Tasks

| Task | Status | Description |
|------|--------|-------------|
| **Object Detection** | ✅ Implemented | Detect and classify objects with bounding boxes |
| **Classification** | 🚧 Pending | Image classification into predefined categories |
| **Segmentation** | 🚧 Pending | Instance segmentation with pixel-level masks |
| **Pose Estimation** | 🚧 Pending | Detect human keypoints and poses |
| **Oriented Bounding Boxes (OBB)** | 🚧 Pending | Rotated bounding boxes for aerial/satellite imagery |

### Supported Modes

| Mode | Status | Description |
|------|--------|-------------|
| **Image** | ✅ Implemented | Upload and process single images |
| **Video** | 🚧 Pending | Process video files frame-by-frame |
| **Webcam (Live)** | 🚧 Pending | Real-time inference from webcam feed |

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)
- 2GB+ RAM recommended

## 🛠️ Installation & Setup

### Using Docker Compose (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd yolo-playground
   ```

2. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Frontend UI: http://localhost:9700
   - Orchestrator API: http://localhost:9600/docs
   - Vision API: http://localhost:9500/docs

### Local Development

Each service can be run independently. See individual service READMEs for details:
- [Frontend Service](services/frontend/README.md)
- [Orchestrator Service](services/orchestrator/README.md)
- [Vision Service](services/vision/README.md)

## 📖 Usage

1. Open the frontend at http://localhost:9700
2. Select inference mode (Image/Video/Webcam)
3. Select task type (Detect/Classify/Segment/Pose/OBB)
4. Upload an image or start webcam
5. View annotated results in real-time

### API Usage

#### Object Detection Example
```bash
curl -X POST "http://localhost:9600/api/v1/tasks/detect" \
  -F "file=@image.jpg" \
  -o result.jpg
```

## 🔧 Configuration

### Environment Variables

**Vision Service**
- `MODEL_VERSION`: YOLO model version (default: `yolo11n`)

**Orchestrator Service**
- `VISION_SERVICE_HOST`: Vision service hostname (default: `vision`)
- `VISION_SERVICE_PORT`: Vision service port (default: `8000`)

**Frontend Service**
- `ORCHESTRATOR_SERVICE_HOST`: Orchestrator hostname (default: `orchestrator`)
- `ORCHESTRATOR_SERVICE_PORT`: Orchestrator port (default: `8000`)

### Supported Model Versions

- `yolo11n` - Nano (fastest, smallest)
- `yolo11s` - Small
- `yolo11m` - Medium
- `yolo11l` - Large
- `yolo11x` - Extra Large (slowest, most accurate)

## 📁 Project Structure

```
yolo-playground/
├── common/                      # Shared code across services
│   ├── schemas/                 # Pydantic models
│   │   ├── enums.py            # Enums (Task, Mode, ModelVersion)
│   │   ├── requests.py         # Request schemas
│   │   ├── responses.py        # Response schemas
│   │   └── results.py          # Result models (boxes, masks, etc.)
│   └── utils/
│       └── convert.py          # Image conversion utilities
├── services/
│   ├── frontend/               # Streamlit UI
│   ├── orchestrator/           # Middleware service
│   └── vision/                 # YOLO inference engine
└── docker-compose.yml          # Multi-service orchestration
```

## 🧪 Testing

```bash
# Test vision service health
curl http://localhost:9500/health

# Test orchestrator service health
curl http://localhost:9600/health

# View API documentation
# Vision: http://localhost:9500/docs
# Orchestrator: http://localhost:9600/docs
```

## 📝 API Documentation

Interactive API documentation is available via Swagger UI:
- **Vision Service**: http://localhost:9500/docs
- **Orchestrator Service**: http://localhost:9600/docs

## 🚧 Pending Features & TODOs

### High Priority
- [ ] Complete classification task implementation
- [ ] Complete segmentation task implementation
- [ ] Complete pose estimation task implementation
- [ ] Complete OBB (Oriented Bounding Box) task implementation
- [ ] Implement video file processing
- [ ] Implement real-time webcam inference

### Medium Priority
- [ ] Add batch processing support
- [ ] Implement model caching and optimization
- [ ] Add confidence threshold configuration
- [ ] Add NMS (Non-Maximum Suppression) threshold tuning
- [ ] Support for custom trained models

### Low Priority
- [ ] Add result export functionality (JSON, CSV)
- [ ] Performance metrics dashboard
- [ ] Model comparison feature
- [ ] Add unit tests and integration tests
- [ ] CI/CD pipeline setup

### Known Issues
- Video mode UI placeholder implemented but not functional
- Webcam mode commented out (requires streamlit-webrtc)
- Classification endpoint returns empty results
- Segmentation endpoint returns empty results
- Pose endpoint returns empty results
- OBB endpoint returns empty results

## 🛠️ Technology Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **ML Framework**: Ultralytics YOLO11, ONNX Runtime
- **Image Processing**: OpenCV, NumPy
- **HTTP Client**: httpx, requests
- **Containerization**: Docker, Docker Compose

## 📄 License

[Add license information here]

## 👥 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support/contact information here]
