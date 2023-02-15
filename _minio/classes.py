from minio import Minio
from utils.progress import Progress


class MinioExceptions(Exception):
    def __init__(self, message, errors, location=""):
        super().__init__(message)
        self.errors = errors
        self.location = location


class MinioValidators():
    def __init__(self, client):
        self.client = client

    # def connection(self):
    #     errors = []
    #     if self.code == "InvalidAccessKeyId":
    #         errors.append({
    #             "ErrorCode": self.code,
    #             "ErrorMssg": f"The AccessKey ({self.access_key}) you provided does not exist in the records"
    #         })
    #     if self.code == "SignatureDoesNotMatch":
    #         errors.append({
    #             "ErrorCode": self.code,
    #             "ErrorMssg": f"The request SecretKey ({self.secret_key}) does not match the signature you provided, check Key & Signin method"
    #         })
    #     if errors:
    #         raise MinioExceptions("Connection Error:", errors)
    #     if self.code == "AccessDenied":
    #         errors.append({
    #             "ErrorCode": self.code,
    #             "ErrorMssg": f"The current user is not compatible with the given keys or those keys have no access to the bucket requested ({self.resource}), make sure the logged user is the same who has this accessKey ({self.access_key}) and secretKey ({self.secret_key})"
    #         })
    #     if errors:
    #         raise MinioExceptions("Access Error:", errors)
    #     if self.code == "NoSuchBucket":
    #         errors.append({
    #             "ErrorCode": self.code,
    #             "ErrorMssg": f"The specified bucket does not exist ({self.resource})"
    #         })
    #     if errors:
    #         raise MinioExceptions("Request Error:", errors)

    def isObjectExist(self, object_name, bucket_name) -> bool:
        # TODO: get_object to be used
        objects = self.client.list_objects(bucket_name)
        objects_names = [obj.object_name for obj in objects]
        return object_name in objects_names


class MinioOperations():
    def __init__(self, bucket_name, server_play_ground, access_key, secret_key):
        self.bucket_name = bucket_name
        self.server_play_ground = server_play_ground
        self.access_key = access_key
        self.secret_key = secret_key
        self.client = Minio(
            server_play_ground,
            access_key=access_key,
            secret_key=secret_key,
            # just for http connection
            secure=False
        )
        self.validator = MinioValidators(self.client)

    def download(self, object_name):
        self.client.fget_object(
            self.bucket_name, object_name, object_name, progress=Progress())
        print(f"\n {object_name} Downloaded !")

    def isModelInMinio(self, model_name) -> bool:
        return self.validator.isObjectExist(model_name, self.bucket_name)
