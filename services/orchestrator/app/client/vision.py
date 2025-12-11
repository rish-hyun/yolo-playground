from enum import StrEnum
from typing import Dict

import httpx

from common.schemas.requests import ImageFile
from common.schemas.responses import (
    ClassificationResponse,
    DetectionResponse,
    OBBResponse,
    PoseResponse,
    SegmentResponse,
)


class Endpoints:
    CLASSIFY = "/classify"
    DETECT = "/detect"
    OBB = "/obb"
    POSE = "/pose"
    SEGMENT = "/segment"


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"


class VisionClient:

    def __init__(self, host: str = "host.docker.internal", port: int = 9500) -> None:
        self._client = httpx.AsyncClient(base_url=f"http://{host}:{port}/api/v1")

    async def request(
        self,
        method: HttpMethod,
        endpoint: str,
        file: ImageFile,
    ) -> Dict:
        response = await self._client.request(
            method=method.value,
            url=endpoint,
            files={"file": file},
        )
        response.raise_for_status()
        return response.json()

    async def classify(self, file: ImageFile) -> ClassificationResponse:
        response = await self.request(HttpMethod.POST, Endpoints.CLASSIFY, file)
        return ClassificationResponse.model_validate(response)

    async def detect(self, file: ImageFile) -> DetectionResponse:
        response = await self.request(HttpMethod.POST, Endpoints.DETECT, file)
        return DetectionResponse.model_validate(response)

    async def obb(self, file: ImageFile) -> OBBResponse:
        response = await self.request(HttpMethod.POST, Endpoints.OBB, file)
        return OBBResponse.model_validate(response)

    async def pose(self, file: ImageFile) -> PoseResponse:
        response = await self.request(HttpMethod.POST, Endpoints.POSE, file)
        return PoseResponse.model_validate(response)

    async def segment(self, file: ImageFile) -> SegmentResponse:
        response = await self.request(HttpMethod.POST, Endpoints.SEGMENT, file)
        return SegmentResponse.model_validate(response)
