import os.path as path


class SystemOperations():
    def __init__(self):
        pass

    def isModelDownloaded(self, model_store, model_name, model_extension) -> bool:
        if path.exists(path.join(model_store, model_name + model_extension)):
            return True
        return False
