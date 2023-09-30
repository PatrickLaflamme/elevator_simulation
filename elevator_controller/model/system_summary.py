import sys

from pydantic import BaseModel


class SystemSummary(BaseModel):
    min: int = sys.maxsize
    max: int = -1
    sum: int = 0
    n: int = 0
