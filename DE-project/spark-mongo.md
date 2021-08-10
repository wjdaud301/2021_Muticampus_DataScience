## Trouble Shooting

Spark가 `com.mongodb.spark.sql.DefaultSource`패키지를 찾을 수 없는 오류

```
py4j.protocol.Py4JJavaError: An error occurred while calling o56.load.
: java.lang.ClassNotFoundException: Failed to find data source: com.mongodb.spark.sql.DefaultSource. Please find packages at http://spark.apache.org/third-party-projects.html
```



해결책 :

spark와 mongo 사이에 processing이 필요할 땐 **jar**들이 필요한데 버전영향을 많이 받는다.

따라서 나의 Spark버전에 맞는 MongoDB Spark Connector를 다운받는다.

1. MongoDB Spark Connector를 다운 ( https://spark-packages.org/package/mongodb/mongo-spark )
2. wget 명령어로 ubuntu에서 다운

```
/$SPARK_HOME/jars directory 이동 후

>wget https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.1/mongo-spark-connector_2.12-3.0.1.jar
```

| Mongo-Spark | Spark |
| ----------- | ----- |
| 3.0.1       | 3.0.x |
| 2.4.3       | 2.4.x |
| 2.3.5       | 2.3.x |
| 2.2.9       | 2.2.x |
| 2.1.8       | 2.1.x |



3. 추가 jars download
   mongo-java-driver : https://mvnrepository.com/artifact/org.mongodb/mongo-java-driver/3.11.2

   ```
   >wget https://repo1.maven.org/maven2/org/mongodb/mongo-java-driver/3.11.2/mongo-java-driver-3.11.2.jar
   ```

   

   bson : https://mvnrepository.com/artifact/org.mongodb/bson/3.11.2

   ```
   >wget https://repo1.maven.org/maven2/org/mongodb/bson/3.11.2/bson-3.11.2.jar
   ```

   

참고 : https://qkqhxla1.tistory.com/1115 (mongoDB - spark - aws s3)





---



### PySpark와 MongoDB Connection

```python
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField, StringType, IntegerType

# conf = SparkConf()
# conf.set('spark.jars.packages', "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1")
# spark = SparkSession.builder.appName("multi").config(conf=conf).getOrCreate()

spark = SparkSession \
    .builder \
    .appName("multi") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017") \
    .config("spark.mongodb.input.database","datalake") \
    .config("spark.mongodb.input.collection", "i") \
    .config("packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .getOrCreate()

sc =spark.sparkContext
```



### 스키마 생성

```python
subwaySchema =  StructType([
    StructField("USE_DT", StringType(),True),
    StructField("LINE_NUM", StringType(),True),
    StructField("SUB_STA_NM", StringType(),True),
    StructField("RIDE_PASGR_NUM", IntegerType(),True),
    StructField("ALIGHT_PASGR_NUM", IntegerType(),True),
    StructField("WORK_DT", StringType(),True),
  ])
```



### 출력

```python
df = spark.read.schema(subwaySchema).format("com.mongodb.spark.sql.DefaultSource").load() 
df.limit(100).show()

+--------+--------+----------------------+--------------+----------------+--------+
|  USE_DT|LINE_NUM|            SUB_STA_NM|RIDE_PASGR_NUM|ALIGHT_PASGR_NUM| WORK_DT|
+--------+--------+----------------------+--------------+----------------+--------+
|20190101|   1호선|                서울역|         39420|           31121|20190104|
|20190101|   1호선|                  시청|         11807|           10322|20190104|
|20190101|   1호선|                  종각|         20944|           16658|20190104|
|20190101|   1호선|               종로3가|         17798|           15762|20190104|
|20190101|   1호선|               종로5가|         13578|           13282|20190104|
|20190101|   1호선|                동대문|          9337|           10457|20190104|
|20190101|   1호선|                신설동|          6832|            6930|20190104|
|20190101|   1호선|                제기동|         10187|           10178|20190104|
|20190101|   1호선|청량리(서울시립대입구)|         15007|           15397|20190104|
|20190101|   1호선|                동묘앞|          8045|            8504|20190104|
|20190101|   2호선|                  시청|          8381|            6049|20190104|
|20190101|   2호선|            을지로입구|         22478|           21330|20190104|
|20190101|   2호선|             을지로3가|          8104|            7554|20190104|
|20190101|   2호선|             을지로4가|          3862|            3728|20190104|
|20190101|   2호선|    동대문역사문화공원|         10995|           11808|20190104|
|20190101|   2호선|                  신당|          6811|            7324|20190104|
|20190101|   2호선|              상왕십리|          5723|            5960|20190104|
|20190101|   2호선|      왕십리(성동구청)|          9379|            8332|20190104|
|20190101|   2호선|                한양대|          2340|            2751|20190104|
|20190101|   2호선|                  뚝섬|          4882|            5204|20190104|
+--------+--------+----------------------+--------------+----------------+--------+
only showing top 20 rows
```



pyspark example: https://sparkbyexamples.com/pyspark/pyspark-read-json-file-into-dataframe/

https://www.mongodb.com/blog/post/getting-started-with-mongodb-pyspark-and-jupyter-notebook

