

class ManagementOperations():
    def __init__(self, management_api) -> None:
        self.management_api = management_api

    def isModelServed(self, model_name) -> bool:
        res = requests
