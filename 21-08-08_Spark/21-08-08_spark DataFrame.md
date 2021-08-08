## 1. 스파크세션 초기화



### 스파크 세션 초기화

---

데이터셋, 데이터 프레임은 스파크 세션을 이용하여 처리 합니다.

```scala
import org.apache.spark.sql.SparkSession

val spark = SparkSession
  .builder()
  .appName("Spark SQL basic example")
  .config("spark.some.config.option", "some-value")
  .getOrCreate()
```



스파크 쉘(spark-shell)을 이용할 경우 REPL쉘이 스파크 세션 객체를 초기화합니다. 스파크 쉘 실행시 스파크 컨텍스트와 스파크 세션을 생성했다는 메세지를 확인할 수 있습니다.

```scala
$ spark-shell --master yarn --queue queue_name
Spark context Web UI available at http://127.0.0.1:4040
Spark context available as 'sc' (master = yarn, app id = application_1520227878653_37974).
Spark session available as 'spark'.
scala> spark
res40: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@21840920
```





### 하이브 메타스토아 연결

---

스파크 세션은 단독으로 사용할 수 있지만, 하이브 메타스토어와 연결하여 사용할 수 있습니다. 스파크 세션 생성시에 `hive.metastore.uris`값을 설정하면 메타스토어와 연결됩니다.

```scala
// hive.metastore.uris 옵션에 하이브 메타스토어 접속 주소를 입력한다. 
val spark = SparkSession.builder().appName("sample").config("hive.metastore.uris", "thrift://hive_metastore_ip:hive_metastore_port").enableHiveSupport().getOrCreate()

// 데이터베이스 조회 
scala> spark.sql("show databases").show()
+-------------+
| databaseName|
+-------------+
|      test_db1|
|      test_db2|
```



---







## 2. 데이터 프레임 초기화



데이터 프레임은 스파크세션의 `read`메소드로 생성할 수 있습니다. `read`는 json, parquet, ocr, text 등 다양한 형식의 데이터를 읽을 수 있습니다. 

스파크 세션을 이용하여 데이터 프레임을 초기화 하는 방법
people.json 파일을 읽어서 데이터 프레임을 생성합니다.

```scala
// json 형식의 데이터 입력 
$ cat people.json
{"name":"Michael"}
{"name":"Andy", "age":30}
{"name":"Justin", "age":19}

val df = spark.read.json("/user/people.json")
scala> df.show()
+----+-------+
| age|   name|
+----+-------+
|null|Michael|
|  30|   Andy|
|  19| Justin|
+----+-------+
```







### RDD를 이용한 데이터 프레임 초기화

---

RDD를 이용해서 데이터 프레임을 생성할 수 있습니다. RDD를 이용한 데이터 초기화는 여러가지 방법이 있습니다. 스키마구조르르 지정할 수도 있고, 지정하지 않으면 스파크에서 임시 칼럼명을 지정합니다.



#### 배열 RDD 데이터를 데이터프레임으로 초기화

단일 데이터의 데이터 프레임 초기화는 다음과 같습니다.

```scala
val wordsRDD = sc.parallelize(Array("a", "b", "c", "d", "a", "a", "b", "b", "c", "d", "d", "d", "d"))
val wordsDF = wordsRDD.toDF()

// 데이터 프레임 확인 
scala> wordsDF.show()
+-----+
|value|
+-----+
|    a|
|    b|
|    c|
|    d|
|    a|
|    a|
|    b|
|    b|
|    c|
|    d|
|    d|
|    d|
|    d|
+-----+

// 칼럼명을 지정했을 때 
val wordsDF = wordsRDD.toDF("word")
scala> wordsDF.show()
+----+
|word|
+----+
|   a|
|   b|
|   c|
|   d|
|   a|
|   a|
|   b|
|   b|
|   c|
|   d|
|   d|
|   d|
|   d|
+----+
```





#### 복합구조의 RDD를 데이터 프레임으로 초기화

----

칼럼이 여러개인 데이터를 이용하여 데이터 프레임을 초기화는 다음과 같습니다.

```scala
val peopleRDD = sc.parallelize(
  Seq( ("David", 150),
       ("White", 200),
       ("Paul",  170) )
)

val peopleDF = peopleRDD.toDF("name", "salary")
scala> peopleDF.show()
+-----+------+
| name|salary|
+-----+------+
|David|   150|
|White|   200|
| Paul|   170|
+-----+------+
```





#### 스키마를 생성하여 데이터 프레임 초기화

---

스키마를 이용하여 데이터를 검증하면서 데이터 프레임을 초기화하 하는 방법은 다음과 같습니다.

```scala
import org.apache.spark.sql._
import org.apache.spark.sql.types._


// RDD를 Row로 초기화 
val peopleRDD = sc.parallelize(
  Seq(
       Row("David", 150),
       Row("White", 200),
       Row("Paul",  170)
  )
)

// RDD를 데이터프레임으로 변형하기 위한 스키마 생성
val peopleSchema = new StructType().add(StructField("name",   StringType, true)).add(StructField("salary", IntegerType, true))

// 데이터 프레임 생성 
val peopleDF = spark.createDataFrame(peopleRDD, peopleSchema)

scala> peopleDF.show()
+-----+------+
| name|salary|
+-----+------+
|David|   150|
|White|   200|
| Paul|   170|
+-----+------+
```





### 외부 데이터를 읽어서 데이터 프레임 초기화

---

외부 데이터를 읽어서 데이터 프레임을 초기화 할 수도 있습니다. json 형태의 파일은 구조를 가지고 있기 때문에 자동으로 스키마를 생성합니다. txt 형태의 파일은 구조가 없기 때문에 스키마를 생성하여 초기화 합니다.



#### TXT 파일을 이용한 데이터 프레임 초기화

---

TXT 파일은 다음의 예제 처럼 읽은 데이터를 구조화하여 RDD로 생성하고 , 스키마를 생성하여 초기화 

```scala
val peopleRDD = sc.textFile("/user/people.txt")
val peopleSchema = new StructType().add(StructField("name",   StringType, true)).add(StructField("age", IntegerType, true))
val sepPeopleRdd = peopleRDD.map(line => line.split(",")).map(x => Row(x(0), x(1).trim.toInt))
val peopleDF = spark.createDataFrame(sepPeopleRdd, peopleSchema)

scala> peopleDS.show()
+----+---+
|name|age|
+----+---+
|   A| 29|
|   B| 30|
|   C| 19|
|   D| 15|
|   F| 20|
+----+---+ㄴㅊ미
```





#### JSON 파일을 이용한 데이터 프레임 초기화

---

JSON 형태의 파일은 데이터가 구조화 되어 있기 때문에 자동으로 초기화 됩니다.

```scala
$ hadoop fs -cat /user/shs/people.json
{"name":"Michael"}
{"name":"Andy", "age":30}
{"name":"Justin", "age":19}


val peopleDF = spark.read.json("/user/shs/people.json")

scala> peopleDF.show()
+----+-------+
| age|   name|
+----+-------+
|null|Michael|
|  30|   Andy|
|  19| Justin|
+----+-------+
```





---





## 3. 데이터 프레임 연산



#### 스키마 확인

스키마를 확인할 때는 `printSchema`를 이용합니다. 현재 데이터프레임의 구조를 출력합니다.

```scala
val df = spark.read.json("/user/people.json")

// 스키마 출력 
scala> df.printSchema()
root
 |-- age: long (nullable = true)
 |-- name: string (nullable = true)

scala> df.show()
+----+-------+
| age|   name|
+----+-------+
|null|Michael|
|  30|   Andy|
|  19| Justin|
+----+-------+
```





### 조회

---

데이터 조회는 `select`를 이용합니다. 칼럼 데이터에 대한 연산을 하고 싶을때는 달러($) 기호를 이용하여 처리 합니다.

```scala
// name 컬럼만 조회
scala> df.select("name").show()
+-------+
|   name|
+-------+
|Michael|
|   Andy|
| Justin|
+-------+

// name, age순으로 age에 값을 1더하여 조회
scala> df.select($"name", $"age" + 1).show()
+-------+---------+
|   name|(age + 1)|
+-------+---------+
|Michael|     null|
|   Andy|       31|
| Justin|       20|
+-------+---------+
```





#### show() 함수 설정

 조회 결과를 확인하는 show() 함수를 이용할 때 기본적으로 보여주는 데이터의 길이와 칼럼의 사이즈를 제한하여 출력합니다. show() 함수는 아래와 같이 출력하는 라인의 개수와 칼럼 사이즈 조절 여부를 설정할 수 있습니다.

```scala
// show 함수 선언 
def show(numRows: Int, truncate: Boolean): Unit = println(showString(numRows, truncate))

// 사용방법 
scala> show(10, false)
scala> show(100, true)
```





### 필터링

---

필터링은 `filter`를 이용하여 처리합니다.

```scala
// 필터링 처리 
scala> df.filter($"age" > 21).show()
+---+----+
|age|name|
+---+----+
| 30|Andy|
+---+----+

// select에 filter 조건 추가 
scala> df.select($"name", $"age").filter($"age" > 20).show()
scala> df.select($"name", $"age").filter("age > 20").show()
+----+---+
|name|age|
+----+---+
|Andy| 30|
+----+---+
```





### 그룹핑

---

그룹핑은 `groupBy`를 이용하여 처리합니다.

```scala
// 그룹핑 처리 
scala> df.groupBy("age").count().show()
+----+-----+
| age|count|
+----+-----+
|  19|    1|
|null|    1|
|  30|    1|
+----+-----+
```





### 칼럼 추가

---

새로운 칼럼을 추가할 때는 `withColumn`을 이용합니다.

```scala
// age가 NULL일 때는 KKK, 값이 있을 때는 TTT를 출력 
scala> df.withColumn("xx", when($"age".isNull, "KKK").otherwise("TTT")).show()
+----+-------+---+
| age|   name| xx|
+----+-------+---+
|null|Michael|KKK|
|  30|   Andy|TTT|
|  19| Justin|TTT|
+----+-------+---+
```







## 데이터프레임의 SQL을 이용한 데이터 조회

데이터프레임은 SQL 쿼리를 이용하여 데이터를 조회할 수 있습니다. 데이터프레임을 이용하여 뷰를 생성하고, SQL 쿼리를 실행하면 됩니다.



### 뷰생성

---

데이터프레임을 SQL로 조회하기 위해서 데이터 프레임에 이름을 부여해주어야 합니다. `createOrReplacetempView`를 이용하여 데이터프레임을 뷰로 등록하고 , SQL에서 사용합니다.

```scala
val df = spark.read.json("/user/people.json")

// DataFrame으로 뷰를 생성 
df.createOrReplaceTempView("people")

// 스파크세션을 이용하여 SQL 쿼리 작성 
scala> spark.sql("SELECT * FROM people").show()
+----+-------+
| age|   name|
+----+-------+
|null|Michael|
|  30|   Andy|
|  19| Justin|
+----+-------+
```





### SQL 사용

---

생성한 뷰를 이용하여 데이터베이스에 문의하듯이 SQL을 호출하면 됩니다.

```scala
// 조회 조건 추가 
scala> spark.sql("SELECT * FROM people WHERE age > 20").show()
+---+----+
|age|name|
+---+----+
| 30|Andy|
+---+----+

// 그룹핑 추가 
scala> spark.sql("SELECT age, count(1) FROM people GROUP BY age").show()
+----+--------+
| age|count(1)|
+----+--------+
|  19|       1|
|null|       1|
|  30|       1|
+----+--------+

```







---





## 4. 저장/불러오기



### 데이터 저장

---

데이터를 저장할 때는 `save`를 이용합니다.

```scala
val peopleDF = spark.read.json("/user/people.json")
case class People(name: String, age: Long)
val peopleDS = peopleDF.as[People]


peopleDS.write.save("/user/ds")
peopleDF.write.save("/user/df")
```





### 저장 포맷 지정

---

`format`을 이용하여 기본 저장 포맷을 지정할 수 있습니다. json, csv 등의 형식을 기본 제공합니다.

```scala
// 데이터 저장 
peopleDS.select("name").write.format("json").save("/user/ds_1")

// 저장 위치 확인 
$ hadoop fs -ls /user/ds_1/
Found 2 items
-rw-r--r--   2 hadoop hadoop          0 2019-01-24 07:19 /user/ds_1/_SUCCESS
-rw-r--r--   2 hadoop hadoop         53 2019-01-24 07:19 /user/ds_1/part-r-00000-88b715ad-1b5b-480c-8e17-7b0c0ea93e9f.json

// 저장 형식 확인 
$ hadoop fs -text /user/ds_1/part-r-00000-88b715ad-1b5b-480c-8e17-7b0c0ea93e9f.json
{"name":"Michael"}
{"name":"Andy"}
{"name":"Justin"}
```





### 압축 포맷 지정

`option`을 이용하여 압축 포맷을 지정할 수 있습니다. gzip, snappy 등의 형식을 이용할 수 있습니다.

```scala
// snappy 형식 압축 
peopleDS.select("name").write.format("json").option("compression","snappy").save("/user/ds_1")
```





### 테이블 저장

테이블을 저장할 때는 `saveAsTable`을 이용 합니다. 하이브 메타스토어에 연결되어 있다면 메타스토어의 정보를 이용해서 저장합니다.

```
peopleDF.select("name", "age").write.saveAsTable("people")
```





### 불러오기 포맷과 옵션 지정

`format`과 `option`을 이용하여 읽을 파일에 대한 옵션을 설정할 수도 있습니다.

```scala
$ cat people.csv
name,age
david,20
park,15
james,40

val peopleDF = spark.read.format("csv")
.option("sep", ",")
.option("inferSchema", "true")
.option("header", "true").load("/user/people.csv")

scala> peopleDF.show()
+-----+---+
| name|age|
+-----+---+
|david| 20|
| park| 15|
|james| 40|
+-----+---+
```
