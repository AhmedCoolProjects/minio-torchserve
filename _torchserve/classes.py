import requests
import json
import os.path as path
import yaml
from yaml import SafeLoader
from _minio.classes import MinioOperations

UN_VARIABLE = ""

with open("config.yml") as f:
    config = yaml.load(f, Loader=SafeLoader)
with open("temp.yml") as f:
    temp = yaml.load(f, Loader=SafeLoader)

minioOps = MinioOperations(
    bucket_name=config["minio"]["connection"]["bucket_name"],
    server_play_ground=config["minio"]["connection"]["server_play_ground"],
    access_key=temp["access_keys"]["access_key"],
    secret_key=temp["access_keys"]["secret_key"]
)


class TorchserveExceptions(Exception):
    def __init__(self, message, errors, model_name=""):
        super().__init__(message)
        self.errors = errors
        self.model_name = model_name


class TorchserveValidators():
    def __init__(self, host, management_api) -> None:
        self.host = host
        self.management_api = management_api
        self.errors = []
        self.solutions = []

    def isModelValid(self) -> bool:
        pass

    def isModelServed(self, model_name, model_store) -> bool:
        self.errors = []
        self.solutions = []
        res = requests.get(self.management_api + "/models")
        models = res.json()["models"]
        for model in models:
            if model["modelName"] == model_name:
                return True
        self.errors.append({
            "code": 404,
            "message": "Model Not Served"
        })
        self.solutions.append({
            "step": 0,
            "message": "Serve the model from " + model_store
        })
        return False

    def isModelDownloaded(self, model_store, model_name) -> bool:
        if path.exists(path.join(model_store, model_name + ".mar")):
            return True
        self.errors.append({
            "code": 404,
            "message": "Model Not Downloaded"
        })
        self.solutions.append({
            "step": 0,
            "message": "Download the model from MinIO"
        })
        return False

    def isModelInMinIO(self, model_name) -> bool:
        if minioOps.isModelInMinio(model_name + ".mar"):
            return True
        self.errors.append({
            "code": 404,
            "message": "Model Not in MinIO"
        })
        self.solutions.append({
            "step": 0,
            "message": "Add model to MinIO"
        })
        return False

    def displayErrors(self):
        self.solutions.reverse()
        for i in range(len(self.solutions)):
            self.solutions[i]['step'] = i + 1
        match len(self.errors):
            case 1:
                return {"errors": self.errors, "solutions": self.solutions, "automated solution": "add `?auto=y` so we gonna Serve the model directly next time"}
            case 2:
                return {"errors": self.errors, "solutions": self.solutions, "automated solution": "add `?auto=y` so we gonna Download & Serve the model directly next time"}
        return {"errors": self.errors, "solutions": self.solutions}

    def applyAutomatedSolutions(self):
        # TODO: download model from minio
        # TODO: serve model from model_store
        pass


class TorchserveOperations():
    def __init__(self, host, model_store, management_api) -> None:
        self.host = host
        self.model_store = model_store
        self.management_api = management_api
        self.validator = TorchserveValidators(host, management_api)

    def getStatus(self):
        res = requests.get(f"{self.host}/ping")
        return json.loads(res.content)

    def serveModel(self, model_name) -> bool:
        path_to_model = path.join(self.model_store, model_name + ".mar")
        res = requests.post(
            f"{self.management_api}/models?url={path_to_model}")
        if res.status_code == 201:
            print("-------------------------\n")
            print(f"model {model_name} Served !")
            print("-------------------------\n")
            return True
        else:
            # TODO: error handler for torchserve
            print(f"{self.management_api}/models/{path_to_model}")
            return False

    def getPrediction(self, model_name, model_version, features, auto) -> tuple:
        # if model_version:
        #     res = requests.post(
        #         f"{self.host}/predictions/{model_name}/{model_version}", data=features)
        #     return json.loads(res.content)
        if self.validator.isModelServed(model_name, self.model_store):
            res = requests.post(
                f"{self.host}/predictions/{model_name}", data=features)
            return res.json(), True

        # NOTE: model not served
        if self.validator.isModelDownloaded(self.model_store, model_name):
            # if auto == "y":
            #     # Serve model
            #     if self.serveModel(model_name):
            #         res = requests.post(
            #             f"{self.host}/predictions/{model_name}", data=features)
            #         return res.json(), True
            #     return {"errors": False}, True
            return self.validator.displayErrors(), True

        # NOTE: model not downloaded
        if self.validator.isModelInMinIO(model_name):
            return self.validator.displayErrors(), True

        # NOTE: model not in minIO
        return self.validator.displayErrors(), True
