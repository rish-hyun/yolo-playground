import os
from typing import ClassVar, Dict, Iterable, List

import numpy as np
from ultralytics import YOLO
from ultralytics.engine.results import Results

from schemas.enums import ModelVersion, Task

MODEL_SUFFIX: Dict[Task, str] = {
    Task.DETECT: "",
    Task.SEGMENT: "-seg",
    Task.CLASSIFY: "-cls",
    Task.POSE: "-pose",
    Task.OBB: "-obb",
}


class BaseYOLOModel:
    task: ClassVar[Task]

    def __init__(self, model_version: ModelVersion) -> None:
        self._model: YOLO = self.load(model_version)

    @classmethod
    def load(cls, model_version: ModelVersion) -> YOLO:
        _path = f"weights/{model_version}{MODEL_SUFFIX[cls.task]}.{{ext}}"
        pt_model_path = _path.format(ext="pt")
        onnx_model_path = _path.format(ext="onnx")
        if not os.path.exists(onnx_model_path):
            _model = YOLO(pt_model_path, task=cls.task)
            _model.export(format="onnx", dynamic=True)
            os.remove(pt_model_path)
        return YOLO(onnx_model_path, task=cls.task)

    def __call__(
        self,
        images: List[np.ndarray],
        stream: bool = False,
    ) -> Iterable[Results]:
        return self._model(images, stream=stream, verbose=False)
