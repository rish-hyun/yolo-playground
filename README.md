# YOLO Playground

A microservices-based computer vision platform using YOLO (You Only Look Once) models for various vision tasks including object detection, instance segmentation, classification, pose estimation, and oriented bounding boxes.

## Architecture

The platform consists of the following services:

- **Vision Service**: Core AI service that hosts YOLO models and performs inference on uploaded images.
- **Orchestrator Service**: API gateway that coordinates requests between clients and the vision service, handles image annotation.
- **Frontend Service**: Streamlit web interface for uploading images and viewing results (under development).
- **Common**: Shared schemas, utilities, and data models used across services.

## Features

- **Object Detection**: Identify and locate objects in images with bounding boxes.
- **Instance Segmentation**: Detect objects and generate pixel-level masks.
- **Image Classification**: Classify images into predefined categories.
- **Pose Estimation**: Detect human keypoints and poses.
- **Oriented Bounding Boxes (OBB)**: Detect objects with rotated bounding boxes.

## Supported Models

- YOLO11n (nano) variants for different tasks
- ONNX runtime for optimized inference
- Automatic model export from PyTorch to ONNX format

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Running with Docker Compose

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd yolo-playground
   ```

2. Build and start the services:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

3. Access the services:
   - Vision Service API: http://localhost:9500/docs
   - Orchestrator Service API: http://localhost:9600/docs
   - Frontend (Streamlit app, when ready): http://localhost:9700

### Service Ports

- Vision: 9500
- Orchestrator: 9600
- Frontend: 9700 (Streamlit app, planned)

## API Usage

### Vision Service

Direct access to YOLO inference endpoints:

```bash
curl -X POST "http://localhost:9500/api/v1/detect" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg"
```

### Orchestrator Service

Annotated image responses:

```bash
curl -X POST "http://localhost:9600/api/v1/detect" \
     -H "accept: image/jpeg" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg" \
     --output annotated_image.jpg
```

## Development

### Local Development Setup

Each service can be run independently for development:

1. Install Python 3.11+
2. Install service dependencies: `pip install -r requirements.txt`
3. Run the service: `uvicorn main:app --reload`

### Project Structure

```
yolo-playground/
├── common/                    # Shared code
│   ├── schemas/              # Pydantic models
│   └── utils/                # Utility functions
├── services/
│   ├── frontend/             # Web UI (planned)
│   ├── orchestrator/         # API gateway with annotation
│   └── vision/               # YOLO inference service
├── docker-compose.yml        # Multi-service orchestration
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add license information]