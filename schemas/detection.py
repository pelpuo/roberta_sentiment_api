from typing import List
from pydantic import BaseModel
from enum import Enum


class Model(str, Enum):
    yolov3tiny = "yolov3-tiny"
    yolov3 = "yolov3"