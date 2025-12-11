import cv2
import numpy as np

from .color import Color


class Annotator:

    def __init__(self, image: np.ndarray, /) -> None:
        self._image = image.copy()

        self._line_width = max(round(sum(image.shape[:2]) / 2 * 0.003), 2)
        self._thickness = max(self._line_width - 1, 1)
        self._font_face = cv2.FONT_HERSHEY_SIMPLEX
        self._font_scale = self._line_width / 3
        self._line_type = cv2.LINE_AA

    def result(self) -> np.ndarray:
        return self._image

    def draw_box_label(
        self,
        class_id: int,
        label: str,
        confidence: float,
        bbox: tuple[int, int, int, int],
    ) -> None:

        box_color = Color.pick(class_id)
        text_color = Color.dark() if box_color.is_light() else Color.light()

        x1, y1, x2, y2 = bbox
        label = f"{label} {confidence:.2f}"

        cv2.rectangle(
            self._image,
            (x1, y1),
            (x2, y2),
            box_color,
            thickness=self._line_width,
            lineType=self._line_type,
        )

        text_width, text_height = cv2.getTextSize(
            label,
            fontFace=self._font_face,
            fontScale=self._font_scale,
            thickness=self._thickness,
        )[0]
        text_height += 3

        x1 = min(x1, self._image.shape[1] - text_width)
        if y1 >= text_height:
            y2 = y1 - text_height
        else:
            y2 = y1 + text_height

        cv2.rectangle(
            self._image,
            (x1, y1),
            (x1 + text_width, y2),
            box_color,
            -1,
            self._line_type,
        )

        if y1 >= text_height:
            y1 -= 2
        else:
            y1 += text_height - 1

        cv2.putText(
            self._image,
            label,
            (x1, y1),
            self._font_face,
            self._font_scale,
            text_color,
            thickness=self._thickness,
            lineType=self._line_type,
        )
