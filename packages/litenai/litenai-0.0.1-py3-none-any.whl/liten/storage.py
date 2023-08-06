import os
import json
import logging

import boto3
from botocore.config import Config as BotoConfig

from typing import List, Union
from .config import Config
logger = logging.getLogger(__name__)

class Storage:
    """
    Liten Storage Class - Wraps object storage calls to read and write objects. For AWS this would be S3.
    """
    def __init__(self):
        """
        Create and initialize Liten Cache
        """
        self._config = Config()
        # Move these to config yml
        self._max_pool_connections = 400
        self._max_transfer_threads = "50"
        # instantiate a BulkBoto3 object
        self._verbose = True
        self._service_name = "s3"
        self._resource = None
        try:
            boto3_config = BotoConfig(
                signature_version="s3v4",
                max_pool_connections=self._max_pool_connections,
            )
            self._resource = boto3.resource(
                service_name=self._service_name,
                endpoint_url=self._config.s3_endpoint_url,
                aws_access_key_id=self._config.storage_access_key_id,
                aws_secret_access_key=self._config.storage_secret_access_key,
                config=boto3_config,
            )
        except Exception as e:
            logger.exception(f"Cannot connect to object storage. {e}")
            raise
        pass

    def get_bucket(self, bucket_name: str):
        """
        Get a bucket object from bucket name.
        :param bucket_name: Name of the bucket.
        :return: Bucket object.
        """
        return self._resource.Bucket(bucket_name)

    def create_bucket(self, bucket_name: str) -> None:
        """
        Create a new bucket on the object storage.
        :param bucket_name: Name of the bucket.
        """
        try:
            self._resource.create_bucket(Bucket=bucket_name)
            logger.info(f"Successfully created new bucket: '{bucket_name}'.")
        except Exception as e:
            logger.exception(f"Cannot create a new bucket: '{bucket_name}'. {e}")
            raise
        pass

    def empty_bucket(self, bucket_name: str) -> None:
        """
        Delete all objects of a bucket.
        :param bucket_name: Name of the bucket.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            bucket.objects.all().delete()
            logger.info(f"Successfully deleted objects on: '{bucket_name}'.")
        except Exception as e:
            logger.warning(f"Cannot empty bucket: '{bucket_name}'. {e}")
        pass

    def upload_file(self, bucket_name: str, local_path: str, storage_path: str) -> None:
        """
        Upload local file to object storage one by one.
        :param bucket_name: Name of the bucket.
        :param local_path: local file to be uploaded
        :param storage_path: storage path where the file is to be uploaded 
        """
        bucket = self.get_bucket(bucket_name)
        try:
            bucket.upload_file(local_path, storage_path)
            logger.info(
                f"Successfully uploaded {local_path} files to bucket: '{bucket_name}'."
            )
        except Exception as e:
            logger.exception(f"Cannot upload files. {e}")
            raise
        pass

    def download_file(self, bucket_name: str, local_path: str, storage_path: str) -> None:
        """
        Download files from object storage to local path
        :param bucket_name: Name of the bucket
        :param local_path: local file to be downloaded
        :param storage_path: storage path where the file is to be downloaded 
        """
        bucket = self.get_bucket(bucket_name)
        try:
            bucket.download_file(storage_path, local_path)
            logger.info(
                f"Successfully downloaded {local_path} files from bucket: '{bucket_name}'."
            )
        except Exception as e:
            logger.exception(f"Cannot download files. {e}")
            raise

    def check_object_exists(self, bucket_name: str, object_path: str,) -> bool:
        """
        Check if an object exists on the object storage.
        :param bucket_name: Name of the bucket.
        :param object_path: Path of the object to check.
        :return: True if the object exists, False otherwise.
        """
        try:
            self._resource.Object(bucket_name, object_path).load()
            return True
        except Exception as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                logger.exception("Something else has gone wrong.")
                raise

    def list_objects(self, bucket_name: str, storage_dir: str = "") -> List[str]:
        """
        Get the list of all objects in a specific directory on the object storage.
        :param bucket_name: Name of the bucket.
        :param storage_dir: Base directory on the object storage to get list of objects.
        """
        bucket = self.get_bucket(bucket_name)
        return [
            _object.key for _object in bucket.objects.filter(Prefix=storage_dir)
        ]