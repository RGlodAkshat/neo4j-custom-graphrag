from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

user_router = APIRouter()

@user_router.get("/user_route")
async def user_route(file_path: str = Query(None), url: str = Query(None)):
    if file_path:
        return JSONResponse(content={"message": f"Received file path: {file_path}"})
    elif url:
        return JSONResponse(content={"message": f"Received URL: {url}"})
    else:
        return JSONResponse(
            content={"error": "Please provide either a file_path or a url parameter."},
            status_code=400
        )
