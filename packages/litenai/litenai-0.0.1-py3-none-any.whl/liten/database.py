from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import *

import re

"""
Liten Database
"""
import pyspark
from pyspark.sql import SparkSession

class Database:
    """
    Liten Database Class - Uses delta lake to store Liten database.
                           For now all data is loaded as a table from csv file
    """
    def __init__(self, spark):
        """
        Create and initialize Liten Cache
        """
        self._spark = spark
        self._data_bucket = 's3a://data'
        self._work_bucket = 's3a://work'
        self._model_bucket = 's3a://model'
        # standardized timestamp field name
        self._time_field = 'time'
        pass

    @property
    def time_field(self):
        """
        Return time_field
        """
        return self._time_field
    
    @property
    def spark(self):
        """
        Return spark
        """
        return self._spark
