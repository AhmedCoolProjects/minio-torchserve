from minio import Minio


class MinioClientOperations():
    def __init__(self, server_play_ground, access_key, secret_key):
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

    def isObjectInMinIO(self, bucket_name, object_name) -> bool:
        try:
            self.client.get_object(bucket_name, object_name)
            return True
        except:
            return False
