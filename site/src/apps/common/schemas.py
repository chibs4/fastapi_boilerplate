import ujson
from pydantic import BaseModel as PydanticModel


# Base config for all schemas.
class BaseModel(PydanticModel):
    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        orm_mode = True
        min_anystr_length = 1
