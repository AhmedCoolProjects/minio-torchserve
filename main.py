from typing import Union
from fastapi import FastAPI, Request, status, Response
from _torchserve.inference import InferenceOperations
from constants import ModelRequestErrors
import yaml
from yaml.loader import SafeLoader

app = FastAPI()

with open("config.yml") as f:
    config = yaml.load(f, Loader=SafeLoader)


inferenceAPI = InferenceOperations(
    config["torchserve"]["inference_api"], config["torchserve"]["model_store"])
modelErrorsAPI = ModelRequestErrors()


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


@app.get("/api/ismodelserved/{model_name}")
def ismodelserved(response: Response, model_name):
    if inferenceAPI.isModelServed(model_name):
        return {"data": True, "error": {}}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": False, "error": modelErrorsAPI.MNS()}


@app.get("/api/ismodelinstore/{model_name}")
def ismodelinstore(response: Response, model_name):
    if inferenceAPI.isModelInStore(model_name, config["model"]["model_extension"]):
        return {"data": True, "error": {}}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": False, "error": modelErrorsAPI.MND()}


@app.get("/api/ismodelinminio/{model_name}")
def ismodelinminio(response: Response, model_name):
    if inferenceAPI.isModelInMinio(config["minio"]["client"]["bucket_name"], model_name, config["model"]["model_extension"]):
        return {"data": True, "error": {}}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"data": False, "error": modelErrorsAPI.MNE()}
