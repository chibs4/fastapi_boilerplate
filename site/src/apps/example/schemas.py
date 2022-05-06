from typing import Literal
from datetime import datetime

from apps.common.schemas import BaseModel


class Example(BaseModel):
    id: int
    literal: Literal[1, 2, 3, 4]
    date: datetime
