from schemas.enums import Task

from .base import BaseYOLOModel


class OBBModel(BaseYOLOModel):
    task: Task = Task.OBB
