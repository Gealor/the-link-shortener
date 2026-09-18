from typing import Literal

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/unhandled-error")
async def test_unhandled_error(
    type: Literal["expected", "unexpected"] = Query()
) -> JSONResponse:
    try:
        if type=="expected":
            raise ValueError()
        else:
            raise KeyError(type)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This is handled exception",
        ) from e
