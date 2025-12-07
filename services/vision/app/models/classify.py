from schemas.enums import Task

from .base import BaseYOLOModel


class ClassificationModel(BaseYOLOModel):
    task: Task = Task.CLASSIFY
