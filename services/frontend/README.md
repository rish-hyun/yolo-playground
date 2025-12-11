# Frontend Service

The Frontend Service provides a web-based user interface for the YOLO Playground platform using Streamlit. It allows users to upload images, select vision tasks, and view annotated results through an intuitive web application.

## Features (Planned)

- **Image Upload**: File uploader interface for uploading images
- **Task Selection**: Select from available vision tasks (detection, segmentation, etc.)
- **Real-time Processing**: Live preview of annotated results
- **Batch Processing**: Process multiple images simultaneously
- **Result Visualization**: Interactive display of detection results
- **Download Options**: Export annotated images and result data

## Technology Stack

- **Framework**: Streamlit
- **API Integration**: HTTP requests to Orchestrator Service
- **Image Processing**: PIL/Pillow for image handling
- **UI Components**: Streamlit native widgets and components

## Configuration

### Environment Variables

- `ORCHESTRATOR_HOST`: Orchestrator service hostname (default: "localhost")
- `ORCHESTRATOR_PORT`: Orchestrator service port (default: "9600")

## Dependencies

- `streamlit`: Web app framework
- `requests`: HTTP client for orchestrator communication
- `pillow`: Image processing
- `numpy`: Array operations for image data

## User Interface

### Main Features

1. **Upload Area**: File uploader for image files
2. **Task Selector**: Sidebar or dropdown to choose vision task
3. **Preview Panel**: Before/after image display
4. **Results Panel**: Detection results and confidence scores
5. **Download Section**: Options to save annotated images

### Supported Formats

- JPEG, PNG, BMP, TIFF images
- Maximum file size: 10MB per image
- Batch upload: Up to 10 images simultaneously

## Running Locally

1. Ensure Orchestrator Service is running

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```bash
   export ORCHESTRATOR_HOST="localhost"
   export ORCHESTRATOR_PORT="9600"
   ```

4. Run the Streamlit app:
   ```bash
   streamlit run app/main.py --server.port 9700 --server.address 0.0.0.0
   ```

5. Access the web interface at: http://localhost:9700

## Docker

Build and run with Docker:

```bash
docker build -t frontend-service .
docker run -p 9700:8501 \
  -e ORCHESTRATOR_HOST="orchestrator" \
  -e ORCHESTRATOR_PORT="8000" \
  frontend-service
```

## Development Status

**Note**: The frontend service is currently under development. The code structure is planned but not yet implemented. This documentation describes the intended functionality assuming the service is operational.

### Planned Architecture

- `app/main.py`: Main Streamlit application
- `components/`: Reusable Streamlit components
- `utils/`: Helper functions for API calls and image processing
- `config.py`: Configuration and environment variable handling