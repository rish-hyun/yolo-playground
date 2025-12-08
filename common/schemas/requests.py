from typing import NamedTuple

from pydantic import BaseModel


class VisionFile(NamedTuple):
    file_name: str
    file_content: bytes
    content_type: str


class VisionRequest(BaseModel):
    file: VisionFile
