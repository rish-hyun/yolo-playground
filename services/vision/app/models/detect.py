from schemas.enums import Task

from .base import BaseYOLOModel


class DetectionModel(BaseYOLOModel):
    task = Task.DETECT
