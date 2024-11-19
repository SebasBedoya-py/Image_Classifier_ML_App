import os
from typing import List

from app import db
from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    """
    Endpoint to predict the class of an uploaded image using the ML model.
    
    Parameters:
    -----------
    file : UploadFile
        The image file uploaded by the user
    current_user : 
        The authenticated user making the request
        
    Returns:
    --------
    dict
        success: bool - Whether the prediction was successful
        prediction: str - The predicted class name
        score: float - Confidence score of the prediction
        image_file_name: str - Hash of the processed image
    
    Raises:
    -------
    HTTPException
        400 - If file type is not supported
    """
    
    rpse = {"success": False, "prediction": None, "score": None}
    
    # Check if file sended is an image and create hash name
    allowed_file = utils.allowed_file(file.filename)
    file_hash = await utils.get_file_hash(file)
    
    # Send the file to be processed by the model.
    file_path = os.path.join(config.UPLOAD_FOLDER, file_hash)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    prediction, score = await model_predict(file_hash)
    
    # Return `rpse` dict with the corresponding values
    if allowed_file == True:
        rpse["success"] = True
        rpse["prediction"] = prediction
        rpse["score"] = score
        rpse["image_file_name"] = file_hash
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type is not supported."
        )

    return rpse