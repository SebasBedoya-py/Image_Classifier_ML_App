import json
import time
from uuid import uuid4

import redis

from .. import settings


# Connect to Redis and assign to variable `db``

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


async def model_predict(image_name):
    """
    Queues an image prediction job into Redis and waits for the result.
    
    This function creates a unique job ID, sends the image processing request
    to the ML service via Redis queue, and polls for the results. It implements
    a producer-consumer pattern where this function acts as the producer.

    Parameters
    ----------
    image_name : str
        Name/hash of the uploaded image file stored on disk

    Returns
    -------
    tuple(str, float)
        prediction: The model's predicted class name
        score: Confidence score between 0 and 1
        
    """
    
    print(f"Processing image {image_name}...")
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue.
    job_id = str(uuid4())

    # Create a dict with the job data we will send through Redis
    job_data = {"id": job_id, "image_name": image_name}

    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))
    
    # Loop until we received the response from our ML model
    while True:

        output = db.get(job_id)

        # Check if the text was correctly processed by our ML model
        if output is not None:
            output = json.loads(output)
            prediction = output["prediction"]
            score = output["score"]

            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return str(prediction), float(score)