from fastapi import APIRouter


# from .responses import with_errors


from apps.example.schemas import Example

default_router = APIRouter()


@default_router.post("/example_route", response_model=int)
async def exaple_route(example_params: Example):
    """Рут."""
    return example_params.literal
