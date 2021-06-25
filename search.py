import random
import os
import re
import requests
from sys import argv
# configure spark variables
from pyspark.context import SparkContext
from pyspark.sql.context import SQLContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import regexp_extract
from pyspark.sql.functions import col
from pyspark.sql import Row
from pyspark.sql.functions import sum as spark_sum

# //   127.0.0.1 - - [21/Jul/2014:9:55:27 -0800] "GET /home.html HTTP/1.1" 200 2048
#  //                          1:IP  2:client 3:user 4:date time           5:method 6:req 7:proto   8:respcode 9:size
LOG_PATTERN = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+) (\S+)" (\d{3}) (\d+)'

# configure spark variables
sc = SparkContext()
sqlContext = SQLContext(sc)
spark = SparkSession(sc)

#Input File Path
logFile = '/log_data_flask/generated.txt'

# The below function is modelled specific to Apache Access Logs Model, which can be modified as per needs to different Logs format
# Returns a dictionary containing the parts of the Log
def parse_apache_log_line(logline):
    match = re.search(LOG_PATTERN, logline)
    if match is None:
        raise Error("Invalid logline: %s" % logline)
    return Row(
        ip_address    = match.group(1),
        client_identd = match.group(2),
        user_id       = match.group(3),
        date          = (match.group(4)[:-6]).split(":", 1)[0],
        time          = (match.group(4)[:-6]).split(":", 1)[1],
        method        = match.group(5),
        endpoint      = match.group(6),
        protocol      = match.group(7),
        response_code = int(match.group(8)),
        content_size  = int(match.group(9))
    )

# # .cache() - Persists the RDD in memory, which will be re-used again
# access_logs = (sc.textFile(logFile)
#                .map(parse_apache_log_line)
#                .cache())

# schema_access_logs = sqlContext.createDataFrame(access_logs)
# #Creates a table on which SQL like queries can be fired for analysis
# schema_access_logs.registerTempTable("logs")

# endpointsSearch = (sqlContext
#                 .sql("SELECT * FROM logs WHERE endpoint=" + argv[1])
#                 .rdd.map(lambda row: (row[0], row[1]))
#                 .collect())

url = 'http://localhost:5000/result/'

myobj = {'id': argv[3],
         'content': 'endpointsSearch'}


x = requests.post(url, data = myobj)