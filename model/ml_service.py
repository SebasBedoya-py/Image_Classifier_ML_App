import json
import os
import time

import numpy as np
import redis
import settings
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import decode_predictions, preprocess_input
from tensorflow.keras.preprocessing import image


# Create a redis client
try: 
    db = redis.StrictRedis(
        host=settings.REDIS_IP,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB_ID,
        decode_responses=True
    )
    print('Successfully connected to Redis!')
except Exception as e:
    print('There was a problem connecting to Redis: {e}')
    

# Load ML model
model = ResNet50(include_top=True, weights="imagenet")


def predict(image_name):
    """
    Performs image classification using ResNet50 model.
    
    This function loads an image from disk, preprocesses it according to
    ResNet50 requirements, and performs inference to classify the image
    into one of 1000 ImageNet classes.

    Parameters
    ----------
    image_name : str
        Filename of the image to classify (must exist in UPLOAD_FOLDER)

    Returns
    -------
    tuple(str, float)
        class_name: Human-readable class name from ImageNet
        pred_probability: Confidence score (0-1) rounded to 4 decimal places
        
    Notes
    -----
    - Images are resized to 224x224 pixels
    - Preprocessing includes RGB scaling to [-1, 1]
    """

    # Apply preprocessing
    img_path = os.path.join(settings.UPLOAD_FOLDER, image_name)
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    x = preprocess_input(img_array)

    # Get predictions and decode predictions
    preds = model.predict(x)
    decoded_preds = decode_predictions(preds, top=1)[0]
    class_name = decoded_preds[0][1]

    # Convert probabilities to float and round it
    pred_probability = round(float(decoded_preds[0][2]), 4)
    
    return class_name, pred_probability


def classify_process():
    """
    Main ML service loop that processes image classification requests.
    
    This function implements a consumer pattern that:
    1. Continuously monitors a Redis queue for new classification jobs
    2. Dequeues jobs using BRPOP (blocking right pop)
    3. Extracts job details from JSON payload
    4. Performs image classification using ResNet50
    5. Stores results back in Redis using original job ID as key
    
    The function never returns and handles the complete lifecycle of:
    - Job retrieval from queue
    - Image classification
    - Result storage
    - Error handling
    """
    while True:

        # Take a new job from Redis
        job = db.brpop(settings.REDIS_QUEUE)       
        _, job_value = job
                
        
        # Decode the JSON data for the given job
        decode_json = json.loads(job_value)
        job_id = decode_json.get("id")
        
        # Run the loaded ml model
        class_name, pred_probability = predict(decode_json.get("image_name"))

        # Prepare a new JSON with the results
        output = json.dumps({"prediction": class_name, "score": pred_probability})

        # Store the job results on Redis using the original job ID as the key
        db.set(job_id, output)
        
        # Sleep for a bit
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print("Launching ML service...")
    classify_process()