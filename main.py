import json
from fastapi import FastAPI
from starlette.responses import Response

app = FastAPI()


@app.get("/")
def root(request:Request):
    accept = request.headers.Accept
    if(accept != "text/plain" or accept != "text/html"):
        return Response(content="Accept header should be either text/plain or text/html", status_code=400)
    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    not_found_message = {"detail": f"Page '/{full_path}' not found"}
    return Response(content=json.dumps(not_found_message), status_code=404, media_type="application/json")
