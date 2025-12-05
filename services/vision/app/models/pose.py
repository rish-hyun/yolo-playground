from schemas.enums import Task

from .base import BaseYOLOModel


class PoseModel(BaseYOLOModel):
    task: Task = Task.POSE
