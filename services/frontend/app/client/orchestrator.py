from enum import StrEnum
from typing import Any, Optional

import requests

from common.schemas.requests import ImageFile
from common.schemas.responses import HealthStatus, VisionCapabilitiesResponse


class Endpoints:
    ORCHESTRATOR_HEALTH = "/health"

    VISION_HEALTH = "/api/v1/vision/health"
    CAPABILITIES = "/api/v1/vision/capabilities"

    CLASSIFY = "/api/v1/tasks/classify"
    DETECT = "/api/v1/tasks/detect"
    OBB = "/api/v1/tasks/obb"
    POSE = "/api/v1/tasks/pose"
    SEGMENT = "/api/v1/tasks/segment"


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"


class OrchestratorClient:

    def __init__(self, host: str, port: int) -> None:
        self._base_url = f"http://{host}:{port}"
        self._client = requests.Session()

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
        if file is None:
            return response.json()
        return response.content

    def is_orchestrator_healthy(self) -> bool:
        try:
            response = self.request(
                method=HttpMethod.GET,
                endpoint=Endpoints.ORCHESTRATOR_HEALTH,
            )
            return HealthStatus(**response).healthy
        except Exception as error:
            print(f"Error checking orchestrator health: {error}")
            return False

    def is_vision_healthy(self) -> bool:
        try:
            response = self.request(
                method=HttpMethod.GET,
                endpoint=Endpoints.VISION_HEALTH,
            )
            return HealthStatus(**response).healthy
        except Exception as error:
            print(f"Error checking vision health: {error}")
            return False

    def get_capabilities(self) -> VisionCapabilitiesResponse:
        response = self.request(method=HttpMethod.GET, endpoint=Endpoints.CAPABILITIES)
        return VisionCapabilitiesResponse(**response)

    def classify(self, file: ImageFile) -> bytes:
        return self.request(HttpMethod.POST, endpoint=Endpoints.CLASSIFY, file=file)

    def detect(self, file: ImageFile) -> bytes:
        return self.request(HttpMethod.POST, endpoint=Endpoints.DETECT, file=file)

    def obb(self, file: ImageFile) -> bytes:
        return self.request(HttpMethod.POST, endpoint=Endpoints.OBB, file=file)

    def pose(self, file: ImageFile) -> bytes:
        return self.request(HttpMethod.POST, endpoint=Endpoints.POSE, file=file)

    def segment(self, file: ImageFile) -> bytes:
        return self.request(HttpMethod.POST, endpoint=Endpoints.SEGMENT, file=file)
