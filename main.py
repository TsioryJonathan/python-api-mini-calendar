import json
from fastapi import FastAPI, Request
from starlette.responses import Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

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

    #if header_api_key != "12345678":
    #    return JSONResponse(
    #        content={"message": "Incorrect API key"},
    #        status_code=400
    #    )

    with open("welcome.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=200,
        media_type="text/html"
    )

class EventModel(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str

events_store: List[EventModel] = [EventModel(
    name="Hackathon 2025",
    description="Concours de programmation",
    start_date="2025-08-01",
    end_date="2025-08-02"
)]


def serialized_stored_events():
    events_converted = []
    for event in events_store:
        events_converted.append(event.model_dump())
    return events_converted

@app.get("/events")
def list_events():
    return {"events": serialized_stored_events()}

@app.post("/events")
def create_event(events: List[EventModel]):
    for event in events:
        events_store.append(event)
    return {"Events": serialized_stored_events()}
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open ("404.html" , "r" , encoding="utf-8") as file:
        html_content = file.read()

    return Response(
        content=html_content,
        status_code=404,
        media_type="text/html"
    )
