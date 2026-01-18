from schemas import AskRequest, AskResponse
from rag import answer_question
from ingest import ingest_pdf
from contextlib import asynccontextmanager
from pathlib import Path
from prometheus_client import REGISTRY
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Configure Instrumentator after creating the app
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "rag-backend"
    }


@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Only PDF files allowed')

    pdf_path = UPLOAD_DIR/file.filename
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    return {"message": "PDF Uploaded", "path": str(pdf_path)}


@app.post("/index")
async def index_pdf(path: str):
    ingest_pdf(path)
    return {"message": "Document indexed"}


@app.post("/ask", response_model=AskResponse)
def ask_question(req: AskRequest):
    try:
        answer, sources = answer_question(req.question)
        return AskResponse(answer=answer, sources=sources)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=str(e))


@app.get("/metrics-json")
async def metrics_json():
    """Simple JSON view of metrics for debugging"""
    metrics = {}
    for metric in REGISTRY.collect():
        for sample in metric.samples:
            metrics[sample.name] = {
                "value": sample.value,
                "labels": sample.labels
            }
    return metrics
