## 1. PySpark

스파크는 스칼라를 이용한 방법 외에도, Python, R, Java를 이용해서 분석할 수 있습니다. 여기서는 파이썬을 이용하여 스파크를 사용하는 방법을 알아보겠습니다. 먼저 파이썬을 이용하여 스파크를 실행하는 방법을 알아보겠습니다. 이 예제는 `pyspark`를 이용하여 테스트하였습니다.



### 데이터 프레임 생성 

---

데이터프레임을 생성하는 방법을 알아보겠습니다. 파이썬 내부 데이터를 이용하는 방법과 외부 데이터를 읽어서 생성하는 방법이 있습니다.

```python
from pyspark.sql import Row

datas1 = [("foo", 1),("bar", 2)]
datas2 = [ Row(name='Alice', age=5, height=80),
		   Row(name='Alice', age=5, height=80),
		   Row(name='Alice', age=10, height=80)]
		   
# Spark Context를 이용하는 방법
sc.parallelize(datas1).toDF().show()
sc.parallelize(datas2).toDF().show()

# Spark Session을 이용하는 방법
spark.createDataFrame(datas1).show()
sprak.createDataFrame(datas2).show()

# csv 파일 읽기
from pyspark.sql.types import StructType, StructField, StringType
schema = StructType([
	StructField("age", StringType(), True),
	StructField("height", StringType(), True),
	StructField("name", StringType(), True),
])

spark.read.csv("/user/shs/sample.csv").show()
spark.read.csv("/user/shs/samplel.csv", header=False, schema=schema).show()
```







### PySpark와 Hive 연동

---

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("sample").config("hive.metastore.uris", "thrift://ip:port").enableHiveSupport().getOrCreate()
spark.sql("use db_name")
df = sprak.sql("SELECT * FROM table")
df.show()
```





### groupby

---

그룹핑을 이용하여 윈도우 함수를 이용하는 방법을 알아보겠습니다.

```python
df = spark.createDataFrame(datas2)
df.select('age','height').groupby('age').count().show()
+---+-----+
|age|count|
+---+-----+
|  5|    2|
| 10|    1|
+---+-----+
```





### UDF 사용

---

UDF 함수를 사용하는 방법을 알아보겠습니다.

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# UDF 선언
@udf(returnType=StringType())
def get_first(param):
    if param is None:
        return "N"
    return param[0]


from udfs import get_first
from pyspark.sql.functions import col

# UDF를 이용한 조회
df = spark.creatDataFrame(datas2)
df.select(get_first("name")).show()
+---------------+                                                               
|get_first(name)|
+---------------+
|              A|
|              A|
|              A|
+---------------+

# UDF를 이용한 조회, 컬럼명 변경
df.withcolumn("name_first", get_first(col("name"))).show()
+---+------+-----+----------+                                                   
|age|height| name|name_first|
+---+------+-----+----------+
|  5|    80|Alice|         A|
|  5|    80|Alice|         A|
| 10|    80|Alice|         A|
+---+------+-----+----------+

```

