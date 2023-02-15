import requests
from _system.classes import SystemOperations
from _minio.client import MinioClientOperations
from constants import ModelRequestErrors
import yaml
from yaml.loader import SafeLoader

with open("config.yml") as f:
    config = yaml.load(f, Loader=SafeLoader)

with open("temp.yml") as f:
    temp = yaml.load(f, Loader=SafeLoader)

systemAPI = SystemOperations()
minioAPI = MinioClientOperations(config["minio"]["client"]["server_play_ground"], temp["access_keys"]["access_key"],
                                 temp["access_keys"]["secret_key"])
modelErrorsAPI = ModelRequestErrors()


class InferenceOperations():
    def __init__(self, inference_api, model_store) -> None:
        self.inference_api = inference_api
        self.model_store = model_store
        self.error = {}
        self.result = {}

    def sendResponse(self):
        return self.result, self.error

    def isModelServed(self, model_name) -> bool:
        status_code = requests.post(
            f'{self.inference_api}/predictions/{model_name}').status_code
        if status_code == 404:
            return False
        return True

    def getPrediction(self, model_name: str, model_extension, version: str, features, auto: bool) -> tuple:
        if self.isModelServed(model_name):
            res = requests.post(
                f'{self.inference_api}/predictions/{model_name}').json()
            return res, []
        if systemAPI.isModelDownloaded(self.model_store, model_name, model_extension):
            return self.sendResponse()
        if minioAPI.isObjectInMinIO(config["minio"]["client"]["bucket_name"], model_name + config["model"]["model_extension"]):
            return self.sendResponse()
        # NOTE: not exist in minio
        self.error = modelErrorsAPI.MNE()
        return self.sendResponse()
