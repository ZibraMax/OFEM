import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import FEM


class AnalysisRequest(BaseModel):
    job_name: str
    user_id: str
    modelJson: str
    description: str | None = None


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/resources", StaticFiles(directory="resources"), name="resources")


templates = Jinja2Templates(directory="templates")


@app.get("/model/{id}", response_class=HTMLResponse)
def read_item(request: Request, id: str):
    return templates.TemplateResponse("viewer.html", {"request": request, "id": id})


@app.post("/model/{id}/analyze/")
def send_to_analysis(request: AnalysisRequest, id: str):
    json_model = json.loads(request.modelJson)
    json_model["verbose"] = True
    O: FEM.Core = FEM.importJSON(json_model, {"verbose": True})
    O.solutions = []
    msg: str = f"Analysis for {id} in progress {O.description()}"
    print(msg)
    O.solve(False)
    return O.exportJSON()
