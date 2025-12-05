from schemas.enums import Task

from .base import BaseYOLOModel


class SegmentationModel(BaseYOLOModel):
    task: Task = Task.SEGMENT
