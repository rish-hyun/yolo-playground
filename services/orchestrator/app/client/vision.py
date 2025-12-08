from enum import StrEnum
from typing import Dict

import httpx
from common.schemas.requests import VisionFile, VisionRequest
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

    def __init__(self, host: str = "localhost", port: int = 9500) -> None:
        self._client = httpx.AsyncClient(base_url=f"http://{host}:{port}/api/v1")

    async def request(
        self,
        method: HttpMethod,
        endpoint: str,
        vision_file: VisionFile,
    ) -> Dict:
        response = await self._client.request(
            method=method.value,
            url=endpoint,
            files=VisionRequest(file=vision_file).model_dump(),
        )
        response.raise_for_status()
        return response.json()

    async def classify(self, vision_file: VisionFile) -> ClassificationResponse:
        response = await self.request(Endpoints.CLASSIFY, vision_file)
        return ClassificationResponse.model_validate(response)

    async def detect(self, vision_file: VisionFile) -> DetectionResponse:
        response = await self.request(Endpoints.DETECT, vision_file)
        return DetectionResponse.model_validate(response)

    async def obb(self, vision_file: VisionFile) -> OBBResponse:
        response = await self.request(Endpoints.OBB, vision_file)
        return OBBResponse.model_validate(response)

    async def pose(self, vision_file: VisionFile) -> PoseResponse:
        response = await self.request(Endpoints.POSE, vision_file)
        return PoseResponse.model_validate(response)

    async def segment(self, vision_file: VisionFile) -> SegmentResponse:
        response = await self.request(Endpoints.SEGMENT, vision_file)
        return SegmentResponse.model_validate(response)
