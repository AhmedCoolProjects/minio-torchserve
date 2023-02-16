
# TODO: change code

MODEL_NOT_SERVED = {
    "id": 1,
    "type": "ModelNotServedError",
    "message": "model not served yet by torchserve"
}

MODEL_NOT_EXIST = {
    "id": 2,
    "type": "ModelNotExistError",
    "message": "model does not exist in MinIO bucket"
}

MODEL_NOT_DOWNLOADED = {
    "id": 3,
    "type": "ModelNotDownloadedError",
    "message": "model not downloaded yet to torchserve model store"
}


class ModelRequestErrors():
    def __init__(self) -> None:
        pass

    def MNS(self):
        return MODEL_NOT_SERVED

    def MNE(self):
        return MODEL_NOT_EXIST

    def MND(self):
        return MODEL_NOT_DOWNLOADED
