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


class ModelRequestErrors():
    def __init__(self) -> None:
        pass

    def MNS(self):
        return MODEL_NOT_SERVED

    def MNE(self):
        return MODEL_NOT_EXIST
