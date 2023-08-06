from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType, TimestampType
from pyspark.sql.functions import *

import re

from .database import Database

"""
Liten DemoFiles
"""
import pyspark
from pyspark.sql import SparkSession

class DemoFiles:
    """
    Liten DemoFiles - Load demo files as a table from csv file
    """
    def __init__(self, database : Database):
        """
        Create and initialize Liten Cache
        """
        self._db = database
        self._spark = self._db.spark
        self._weblog = 'weblog'
        self._syslog = 'syslog'
        self._emailserviceaccesslog = 'emailaccesslog'
        self._debug = False #modify this flag to enable verbose mode.
        pass

    def init(self):
        """
        Initialize Liten DemoFiles if not already initialized.
        Should be called only once. Used for demo purposes.
        """
        self._init_weblog()
        self._init_linux_syslog()
        if (self._debug):
            print ("parsing email acess log.")
        self._init_emailaccesslog()
        pass

    def _init_weblog(self):
        # For now read csv, in future needs to be a database table
        weblog_schema = StructType([ \
                                     StructField("ip",StringType(),True), \
                                     StructField(self._db.time_field,TimestampType(),True), \
                                     StructField("url",StringType(),True), \
                                     StructField("status", IntegerType(), True) \
                                    ])
        weblog_df = self._spark.read.\
            format('csv').\
            options(header='true').\
            options(delimiter=',').\
            options(timestampFormat='dd/MMM/yyyy:HH:mm:ss').\
            schema(weblog_schema).\
            load("samplelogfiles/simple_weblog.csv")
        weblog_df.createOrReplaceTempView("weblog")
        return

    def _init_emailaccesslog(self):
        """
        For now read csv, in future needs to be a database table
        csv file which has access logs of a email service. 
        Sample line. For more examples, look in samplelogfiles directory.
        2023-05-30 15:49:43,309,imap,machine291.dovecotservice.africa.mail.emailcompany.com,5077 ,14 ,202,[markasspam],/message/scan/id=messagehash6pgp5x598e ,hashun5xjw6zwrdbd ,60 ,[missingmailbox] ,inaccessible file ,bad encoding,74.229.170.153
        service, host, payload, latency, status, API, Q, reqId, CPULatency, ec, EC2, exception, clientIp
        For latest format, check in folder named logfilegenerationscripts.
        FORMATCSV = '%(asctime)s,%(service)s,%(host)s,%(payload)s ,%(latency)s ,%(status)s,[%(api)s],' \
         '/message/%(act)s/id=messagehash%(mes)s ,hash%(requestId)s ,%(CPUlatency)s ,[%(error_code1)s] ' \
         ',%(error_code2)s ,%(exception)s,%(clientip)-15s '

        Notes: #we will be ignoring MilliSecondsLine below field as it should ideally go with 'Time' field.
        Latency and most other time measurements are in milli seconds.
        """
        emailaccesslog_schema = StructType([ \
                                     StructField("time",TimestampType(),True), \
                                     StructField("milliSecondsLine", IntegerType(), True), \
                                     StructField("service", StringType(), True), \
                                     StructField("hostname",StringType(),True), \
                                     StructField("payloadSize", IntegerType(), True), \
                                     StructField("latency", IntegerType(), True), \
                                     StructField("status", IntegerType(), True), \
                                     StructField("api",StringType(),True), \
                                     StructField("messageUrl",StringType(),True), \
                                     StructField("hash",StringType(),True), \
                                     StructField("cpuLatency", IntegerType(), True), \
                                     StructField("errorCode", StringType(), True), \
                                     StructField("detailedErrorCode", StringType(), True), \
                                     StructField("exception", StringType(), True), \
                                     StructField("ip", StringType(), True) \
                                    ])



        emailaccesslog_df = self._spark.read.\
            format('csv').\
            options(header='false').\
            options(delimiter=',').\
            options(timestampFormat='yyyy-MM-dd HH:mm:ss').\
            schema(emailaccesslog_schema).\
            load("samplelogfiles/emailservice/accesslog.csv")
        emailaccesslog_df.createOrReplaceTempView("emailaccesslog")
        return

    def _init_linux_syslog(self):
        # For now read csv, in future needs to be a database table
        # extended ietf format:
        #  timestamp hostname process[pid]: message header message
        # example
        #  Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
        # convert to a csv file like this first
        #  timestamp,hostname,process,pid,message
        # example
        #  Jun 14 15:16:01|combo|sshd(pam_unix)|19939|authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
        syslog_file = open('samplelogfiles/linux_syslog_2k.log', 'r')
        syslog_csv = open('samplelogfiles/linux_syslog_2k.csv', 'w')
        log_line = syslog_file.readline()
        skips=0
        while log_line:
            log_line = log_line.strip()
            # Read log line and convert to csv format
            # sample log: Jun 14 15:16:01 combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
            # output csv: Jun 14 15:16:01|combo|sshd(pam_unix)|19939|authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4
            log = re.findall("([\w]+\s+[0-9]+\s+[0-9:]+)\s+([\w]+)\s+([\w\(\)\-\.\s]+)\[([0-9]+)\]\:\s*(.*)",log_line)
            if len(log)>0:
                f=log[0]
                syslog_csv.write('|'.join(f)+'\n')
            else:
                # Try another log line format with no pid
                # sample log: Jun 15 04:06:20 combo logrotate: ALERT exited abnormally with [1] 
                # output csv: Jun 15 04:06:20|combo|logrotate||ALERT exited abnormally with [1]
                log = re.findall("([\w]+\s+[0-9]+\s+[0-9:]+)\s+([\w]+)\s+([\w\s\.\-\(\)]+)\:\s*(.*)",log_line)
                if len(log)>0:
                    f=log[0]
                    syslog_csv.write(f"{f[0]}|{f[1]}|{f[2]}||{f[3]}\n")
                else:
                    # Skip other log lines
                    skips = skips+1
            log_line = syslog_file.readline()
        syslog_file.close()
        syslog_csv.close()
        if skips>0:
            print(f"skipped {skips} lines")    
        # Create schema and table now
        # TBD need a generic timestamp converter for the two given formats like -
        #syslog_df.select(to_timestamp(syslog_df.timestamp, ('MMM d HH:mm:ss','MMM dd HH:mm:ss'))).collect()
        syslog_schema = StructType([ \
                                     StructField(self._db.time_field,TimestampType(),True), \
                                     StructField("hostname",StringType(),True), \
                                     StructField("process",StringType(),True), \
                                     StructField("pid", IntegerType(), True), \
                                     StructField("message", StringType(), True) \
                                    ])
        # Use inferSchema as true if no schema provided
        syslog_df = self._spark.read.\
            format('csv').\
            options(header='false').\
            options(delimiter='|').\
            options(timestampFormat='MMM d HH:mm:ss').\
            schema(syslog_schema).\
            load("samplelogfiles/linux_syslog_2k.csv")
        syslog_df.createOrReplaceTempView("syslog")
        pass     
