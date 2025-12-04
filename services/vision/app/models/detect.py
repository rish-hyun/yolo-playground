from typing import Iterable

from schemas.enums import Task

from .base import BaseYOLOModel, Results


class DetectModel(BaseYOLOModel):
    task = Task.DETECT

    def process(self, results: Iterable[Results]) -> Iterable[Results]:
        for result in results:
            yield result
