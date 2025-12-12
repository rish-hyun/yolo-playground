from fastapi import APIRouter

from client import vision_client
from common.schemas.responses import (
    HealthStatus,
    VisionCapabilitiesResponse,
    VisionModes,
    VisionTasks,
)

router = APIRouter()


@router.get(
    "/capabilities",
    summary="Get vision model capabilities",
    response_model=VisionCapabilitiesResponse,
)
async def get_capabilities() -> VisionCapabilitiesResponse:
    return VisionCapabilitiesResponse(
        modes=VisionModes(
            image=True,
            video=False,
            webcam=False,
        ),
        tasks=VisionTasks(
            classify=False,
            detect=True,
            obb=False,
            pose=False,
            segment=False,
        ),
    )


@router.get(
    "/health",
    summary="Get vision service health status",
    response_model=HealthStatus,
)
async def get_health() -> HealthStatus:
    try:
        return HealthStatus.model_validate(await vision_client.health())
    except Exception:
        return HealthStatus(
            healthy=False,
            message="Vision service might be starting up or is unreachable.",
        )
