from typing import NamedTuple

from pydantic import BaseModel


class ImageFile(NamedTuple):
    file_name: str
    file_content: bytes
    content_type: str
