from typing import Union
from fastapi import FastAPI, Request, status, Response
from _torchserve.inference import InferenceOperations
import yaml
from yaml.loader import SafeLoader

app = FastAPI()

with open("config.yml") as f:
    config = yaml.load(f, Loader=SafeLoader)


inferenceAPI = InferenceOperations(
    config["torchserve"]["inference_api"], config["torchserve"]["model_store"])


'''Get Predictions'''


@app.post("/api/predict/{model_name}")
async def predict(request: Request, response: Response, model_name: str, v: Union[str, None] = None, auto: Union[str, None] = None):
    features = await request.body()
    result, error = inferenceAPI.getPrediction(
        model_name, config["model"]["model_extension"], v, features, auto == "y")
    if error:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"data": result, "error": error}
    return {"data": result}
