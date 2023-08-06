"""
Liten Session
"""
import re
import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType
from IPython.display import display, Markdown, Latex
from datetime import datetime
import panel as pn
import pandas as pd
import hvplot
import param
import hvplot.pandas

from .openai import OpenAI
from .agent import Agent
from .database import Database
from .chatbot import ChatBot
from .config import Config
from .demofiles import DemoFiles
from .plotdf import PlotDf
from . import utils

class Session:
    """
    Liten Session - keeps track of user work
    """
    def __init__(self):
        """
        Create and initialize Liten Cache
        """
        self._config = Config()
        self._spark = None
        self._init_spark()
        self._register_udfs()
        self._data = Database(self._spark)
        self._agents = {
            'common' : Agent('common',self._spark),
            'weblog' : Agent('weblog',self._spark),
            'syslog' : Agent('syslog',self._spark),
            'emailaccesslog' : Agent('emailaccesslog',self._spark)
        }
        self._agent = self._agents['common']
        self._agents['weblog'].load('work/WeblogAnalyze.ipynb')
        self._agents['syslog'].load('work/SyslogAnalyze.ipynb')
        self._openai = OpenAI()
        pass

    def _init_spark(self):
        """
        Initialize spark session
        """
        # TBD move all spark configs to yml file
        # gives error for now "spark.sql.execution.arrow.enabled", "true"
        spark_config = SparkConf().setMaster("local[2]") \
                                    .setAppName('litendata.com') \
                                    .set("spark.sql.legacy.timeParserPolicy", "LEGACY") \
                                    .set("spark.sql.debug.maxToStringFields", "100") \
                                    .set("spark.hadoop.delta.enableFastS3AListFrom", "true") \
                                    .set("spark.hadoop.fs.s3a.fast.upload", "true") \
                                    .set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
                                    .set("spark.hadoop.fs.s3a.connection.maximum", "1000") \
                                    .set("spark.hadoop.fs.s3a.connection.establish.timeout", self._config.s3_connection_timeout) \
                                    .set("spark.hadoop.fs.s3a.connection.timeout", self._config.s3_connection_timeout) \
                                    .set("spark.hadoop.fs.s3a.endpoint", self._config.s3_endpoint_url) \
                                    .set("spark.hadoop.fs.s3a.access.key", self._config.storage_access_key_id) \
                                    .set("spark.hadoop.fs.s3a.secret.key", self._config.storage_secret_access_key) \
                                    .set("spark.hadoop.fs.s3a.connection.timeout", self._config.s3_connection_timeout) \
                                    .set("spark.hadoop.fs.s3a.path.style.access", "true") \
                                    .set("spark.hadopp.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
                                    .set("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
        self._spark = SparkSession.builder.config(conf=spark_config).getOrCreate()

    def _register_udfs(self):
        """
        Register SQL UDFs commonly used across SQL code
        """
        def get_date():
            """
            Return current local date and time in format YYYY-MM-DD hh:mm:ss[.mmm]
            """
            ct = datetime.now()
            ts = ct.timestamp()
            ts_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            return ts_str
        self._spark.udf.register("GETDATE", get_date, StringType())

        def get_utc_date():
            """
            Return current UTC date and time in format YYYY-MM-DD hh:mm:ss[.mmm]
            """
            ct = datetime.now()
            ts = ct.timestamp()
            ts_str = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            return ts_str
        self._spark.udf.register("GETUTCDATE", get_utc_date, StringType())

    def agent(self, name):
        """
        Return the agent for the given name
        name: name of the agent
        """
        self._agent = self._agents['common']
        if name in self._agents.keys():
            self._agent = self._agents[name]
        else:
            print(f"Unknown agent name {name}. Using common agent")
        return self._agent
    
    @property
    def spark(self):
        """
        Return the spark session
        """
        return self._spark

    def ask(self, prompt):
        """
        Complete the given prompt
        prompt: prompt to complete
        """
        resp = self._openai.complete_prompt_chat(prompt)
        print(resp)
        return
    
    def chatbot(self):
        cbot = ChatBot(self._spark)
        col_panel = cbot.start()
        return col_panel
    
    def _codegen(self, prompt, lang='sql'):
        code_str = None
        if lang == 'sql':
            code_str = self._agent.generate_sql(prompt)
        elif lang == 'python':
            code_str = self._openai.generate_python(prompt)
        return code_str

    def codegen(self, prompt, lang='sql', new_cell=True, run_code=False):
        """
        Generate a SQL query from the given prompt.
        prompt: prompt to generate SQL query
        lang: language to generate code for. valid values are 'sql' and 'python'
        new_cell: if True, create a new notebook cell with the query
        """
        code_str = self._codegen(prompt, lang)
        if code_str is None:
            print(f"Invalid language {lang}")
            return code_str
        
        if lang == 'sql':
            display(Markdown(code_str))
            sql_cmd = f"df=ten.spark.sql(\"\"\"{code_str}\"\"\")\ndf.show()"
            if new_cell:
                utils.create_new_cell(sql_cmd)
            elif run_code:
                print(f"Running the following sql query.\n{sql_cmd}\n")
                df=self._spark.sql(sql_cmd)
                print(f"Total rows in result={df.count()}")
        elif lang == 'python':
            display(Markdown(code_str))
            if new_cell:
                utils.create_new_cell(code_str)
            elif run_code:
                exec(code_str)
        pass

    def plot(self, df, keep_null=False):
        """
        Plot the given dataframe
        df: dataframe to plot
        """
        if df is None:
            print("Invalid dataframe")
            return
        pandas_df = None
        if keep_null:
            pandas_df = df.toPandas()
        else:
            pandas_df = df.na.drop().toPandas()
        if pandas_df is None:
            print("No data in dataframe to plot")
            return
        pandas_df[self._data.time_field] = pd.to_datetime(pandas_df[self._data.time_field])
        explorer_plot = hvplot.explorer(pandas_df)
        return explorer_plot

    def load_local_demofiles(self):
        """
        Initialize Liten Database using local demo files. Use this if demo needed using local files.
        Should be called only once.
        """
        demofiles = DemoFiles(self._data)
        demofiles.init()
        pass
