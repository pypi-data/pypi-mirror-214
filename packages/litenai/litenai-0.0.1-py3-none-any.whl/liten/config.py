import os
from dotenv import load_dotenv, find_dotenv

class Config:
    """
    Base configurations. Currently it expects all environment variables to be set in .env else it will throw an exception. 
    TBD add a config yml file to set the configuration variables
    """
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        # Read local .env to get all the environment settings
        _ = load_dotenv(find_dotenv())
        self._openai_api_key= os.environ["OPENAI_API_KEY"]
        self._minio_data_dir= os.environ["MINIO_DATA_DIR"]
        self._s3_endpoint_url= os.environ["S3_ENDPOINT_URL"]
        self._storage_access_key_id= os.environ["STORAGE_ACCESS_KEY_ID"]
        self._storage_secret_access_key= os.environ["STORAGE_SECRET_ACCESS_KEY"]
        self._pyspark_work_dir= os.environ["PYSPARK_WORK_DIR"]
        # timeout in seconds
        self._s3_connection_timeout = "60"

    @property
    def openai_api_key(self):
        return self._openai_api_key
    
    @property
    def debug(self):
        return self._debug
    
    @property
    def minio_data_dir(self):
        return self._minio_data_dir
    
    @property
    def s3_endpoint_url(self):
        return self._s3_endpoint_url
    
    @property
    def storage_access_key_id(self):
        return self._storage_access_key_id
    
    @property
    def storage_secret_access_key(self):
        return self._storage_secret_access_key
    
    @property
    def pyspark_work_dir(self):
        return self._pyspark_work_dir
    
    @property
    def s3_connection_timeout(self):
        return self._s3_connection_timeout
    
        
