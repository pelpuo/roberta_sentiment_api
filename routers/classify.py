from typing import Dict, List

from fastapi import APIRouter, HTTPException, UploadFile, File

from core.config import roberta

from schemas.detection import Model
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.post("/classify")
async def classify(text: str):
    
    if not text:
        raise HTTPException(status_code=415, detail="No input text was provided")
    
    return JSONResponse(roberta.classify(text))

    