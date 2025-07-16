import json
from fastapi import FastAPI, Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
app = FastAPI()
@app.get("/")
def root(request: Request):
    accept = request.headers.get("Accept",'')
    header_api_key = request.headers.get("x-api-key",'')

    if "text/plain" not in accept and "text/html" not in accept:
        return JSONResponse(
            content={"message": "Accept header should be either text/plain or text/html"},
            status_code=400
        )

    if header_api_key != "12345678":
        return JSONResponse(
            content={"message": "Incorrect API key"},
            status_code=400
        )

    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=200,
        media_type="text/html"
    )

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return JSONResponse(
        content={"detail": f"Page '/{full_path}' not found"},
        status_code=404
    )
