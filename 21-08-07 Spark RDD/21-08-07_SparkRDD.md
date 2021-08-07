## Spark Application

### RDD

---

```scala
// RDD 예제 
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
distData.map(x => if(x >= 3) x else 0).reduce((x, y) => x + y)
```



### DataFrame

---

```scala
// 데이터프레임 예제 
val df = spark.read.json("examples/src/main/resources/people.json")
df.select($"name", $"age").filter($"age" > 20).show()
df.groupBy("age").count().show()
```



### Dataset

---

```scala
// 데이터셋 예제 
val path = "examples/src/main/resources/people.json"
val peopleDS = spark.read.json(path).as[Person]
peopleDS.show()
```



---



### 1. RDD 초기화

RDD는 내부 데이터를 이용하는 방법과 외부 저장소의 데이터를 이용하는 두가지 방법으로 초기화



#### 내부 데이터 이용(Parallelized Collections)

---

내부 데이터를 이용하는 방법은 스파크 컨텍스트의 `parallelize()`메소드를 이용하여 처리합니다.
사용자가 직업 데이터를 입력하여 생성합니다. 생성한 객체는 RDD 타입이고, 해당 객체를 map(), reduce(), filter()등의 RDD 연산을 이용하여 처리할 수 있습니다.

```scala
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
val distData = sc.parallelize(data, 5)  // 파티션 개수 지정 

// 리듀스 처리 - 모든 수 더하기 
scala> distData.reduce((a, b) => a + b)
res26: Int = 15

// 맵으로 3이상일때만 모든수 더하기 
scala> distData.map(x => if(x >= 3) x else 0).reduce((x, y) => x + y)
res27: Int = 12

// 필터를 이용하여 4이상일때만 더하기 
scala> distData.filter(_ >= 4).reduce(_ + _)
res29: Int = 9    
```





#### 외부 데이터 이용

---

외부 데이터를 이용하는 방법은 스파트 컨텍스트의 `textFile()`메소드를 이용하여 처리합니다. 스파크는 HDFS, S3, Hbase등 다양한 파일시스템을 지원합니다. 생성한 객체는 RDD 타입이므로 RDD 연산을 이용하여 처리할 수 있습니다.

```scala
// 로컬파일을 지정하면 워커노드도 동일한 위치에 파일이 있어야 함 
val distFile = sc.textFile("data.txt")
// s3의 파일도 지정가능 
val distFile = sc.textFile("s3://your-bucket/data.txt")
// hdfs의 파일도 지정가능 
val distFile = sc.textFile("hdfs:///user/data.txt")
// 디렉토리를 지정하면 하위의 모든 파일을 처리 
val distFile = sc.textFile("hdfs:///user/")
// 와일드 카드 사용 가능 
val distFile = sc.textFile("hdfs:///user/*.txt")
// 압축파일도 지정 가능 
val distFile = sc.textFile("hdfs:///user/*.gz")

// RDD 객체 생성 확인 
scala> val distFile = sc.textFile("data.txt")
distFile: org.apache.spark.rdd.RDD[String] = data.txt MapPartitionsRDD[10] at textFile at <console>:26
```



---



### 2. RDD 연산

---

DD 연산은 트랜스포메이션과 액션이 있습니다. 트랜스포메이션은 RDD를 이용해서 새로운 RDD를 생성하고, 액션은 RDD를 이용해서 작업을 처리하여 결과를 드라이버에 반환하거나, 파일시스템에 결과를 쓰는 연산입니다.

스파크는 트랜스포메이션을 호출할 때는 작업을 구성하고, 액션이 호출 될 때 실제 계산을 실행합니다.

**예제 과정**

1. csv파일의 데이터를 읽어서 lines라는 RDD 객체를 생성하고,
2.  각 라인의 글자의 개수를 세는 `map` 트랜스포메이션 함수를 호출하고, 
3. 글자 수의 총합을 구하는 `reduce` 액션 함수를 호출합니다. 
4. `map` 함수를 호출할 때는 작업이 진행되지 않고, `reduce` 함수를 호출할 때 클러스터에서 작업이 진행되는 것을 확인 할 수 있습니다.

```scala
// RDD 객체 생성 
scala> val lines = sc.textFile("/user/cctv_utf8.csv")
lines: org.apache.spark.rdd.RDD[String] = /user/shs/cctv_utf8.csv MapPartitionsRDD[7] at textFile at <console>:24

// map() 액션 호출시에는 반응 없음 
scala> val lineLengths = lines.map(s => s.length)
lineLengths: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[8] at map at <console>:26

// reduce 호출시 작업 처리 
scala> val totalLength = lineLengths.reduce((a, b) => a + b)
[Stage 1:> (0 + 0) / 2]
totalLength: Int = 18531244  
```





#### 트랜스포메이션 (Transformations)

---



트랜스포메이션은 RDD를 이용하여 데이터를 변환하고 RDD를 반환하는 작업입니다. 

| 함수                                            | 설명                                                         |
| :---------------------------------------------- | :----------------------------------------------------------- |
| **map**(*func*)                                 | _func_로 처리된 새로운 **데이터셋 반환**                     |
| **filter**(*func*)                              | _func_에서 true를 반환한 값으로 **필터링**                   |
| **flatMap**(*func*)                             | _func_는 배열(혹은 Seq)을 반환하고, 이 배열들을 **하나의 배열**로 반환 |
| **distinct**([*numPartitions*])                 | 데이터셋의 **중복을 제거**                                   |
| **groupByKey**([*numPartitions*])               | **<u>키를 기준</u>**으로 그룹핑 처리. (K, V) 쌍을 처리하여 (K, Iterable)로 반환 |
| **reduceByKey**(*func*, [*numPartitions*])      | **<u>키를 기준</u>**으로 주어진 _func_로 처리된 작업 결과를 (K, V)로 반환 |
| **sortByKey**([*ascending*], [*numPartitions*]) | **<u>키를 기준</u>**으로 정렬                                |



트랜스포메이션은 다음처럼 사용할 수 있습니다. cctvRDD를 이용하여 처리한 트랜스포메이션은 결과값으로 RDD를 **반환**합니다. take 액션이 호출되기 전에는 실제 작업을 진행하지 않습니다.

```scala
// RDD 생성 
scala> val cctvRDD = sc.textFile("/user/cctv_utf8.csv")
cctvRDD: org.apache.spark.rdd.RDD[String] = /user/cctv_utf8.csv MapPartitionsRDD[1] at textFile at <console>:24

// 라인을 탭단위로 분리하여 첫번째 아이템 반환 
scala> val magRDD = cctvRDD.map(line => line.split("\t")(0))
magRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[3] at map at <console>:26

// 중복 제거 
scala> val distRDD = magRDD.distinct()
distRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[9] at distinct at <console>:28

// 중복 제거한 데이터를 10개만 출력 
scala> distRDD.take(10).foreach(println)
성남둔치공영주차장                                                              
울산 동구청
```





#### 액션(Actions)

---



액션은 RDD를 이용하여 작업을 처리한 결과를 반환하는 작업입니다.

| 함수                       | 설명                                                         |
| :------------------------- | :----------------------------------------------------------- |
| **reduce**(*func*)         | _func_를 이용하여 데이터를 집계(두 개의 인수를 받아서 하나를 반환). 병렬처리가 가능해야 함 |
| **collect**()              | 처리 결과를 배열로 반환. 필터링 등 작은 데이터 집합을 반환하는데 유용 |
| **count**()                | 데이터셋의 개수 반환                                         |
| **first**()                | 데이터셋의 첫번째 아이템 반환(take(1)과 유사)                |
| **take**(*n*)              | 데이터셋의 첫번째 부터 _n_개의 배열을 반환                   |
| **saveAsTextFile**(*path*) | 데이터셋을 텍스트 파일로 지정한 위치에 저장                  |
| **countByKey**()           | 키를 기준으로 카운트 반환                                    |
| **foreach**(*func*)        | 데이터셋의 각 엘리먼트를 _func_로 처리. 보통 Accmulator와 함께 사용 |



액션은 다음처럼 사용할 수 있습니다. cctvRDD를 이용하여 처리한 액션은 결과를 드라이버(스파크쉘)에 반환하거나, 파일로 저장할 수 있습니다.

```scala
// RDD 생성
scala> val cctvRDD = sc.textFile("/user/cctv_utf8.csv")
cctvRDD: org.apache.spark.rdd.RDD[String] = /user/cctv_utf8.csv MapPartitionsRDD[1] at textFile at <console>:24


// 첫번째 라인 반환 
scala> cctvRDD.first()
res0: String = 관리기관명    소재지도로명주소    소재지지번주소 설치목적구분  카메라대수   카메라화소수  촬영방면정보  보관일수    설치년월    관리기관전화번호    위도  경도  데이터기준일자 제공기관코드  제공기관명


// 10개의 라인을 출력
scala> cctvRDD.take(10).foreach(println)
관리기관명   소재지도로명주소    소재지지번주소 설치목적구분  카메라대수   카메라화소수  촬영방면정보  보관일수    설치년월    관리기관전화번호    위도  경도  데이터기준일자 제공기관코드  제공기관명
제주특별자치도 제주특별자치도 제주시 동문로9길 3 제주특별자치도 제주시 건입동 1120    생활방범    1       청은환타지아 북측 4가    30      064-710-8855    33.5132891  126.5300275 2018-04-30  6500000 제주특별자치도


// 텍스트 파일로 지정한 위치에 저장 
scala> cctvRDD.saveAsTextFile("/user/cctvRDD")
[Stage 7:>                                                          (0 + 0) / 2]


// 저장한 파일을 확인 
$ hadoop fs -ls /user/cctvRDD/
Found 3 items
-rw-r--r--   2 hadoop hadoop          0 2019-01-22 04:05 /user/cctvRDD/_SUCCESS
-rw-r--r--   2 hadoop hadoop   15333006 2019-01-22 04:05 /user/cctvRDD/part-00000
-rw-r--r--   2 hadoop hadoop   15332503 2019-01-22 04:05 /user/cctvRDD/part-00001
```



---





### 함수 전달

---

RDD 연산을 처리할 때 매번 작업을 구현하지 않고, 함수로 구현하여 작업을 처리할 수도 있습니다

함수를 전달 할 때는 외부의 변수를 이용하지 않는 순수 함수를 이용하는 것이 좋습니다. 클러스터 환경에서 외부 변수의 사용은 잘 못된 결과를 생성할 가능성이 높기 때문입니다.

```scala
// RDD에 map, reduce 함수를 람다함수로 전달
scala> cctvRDD.map(line => line.length).reduce((a, b) => a + b)
res12: Int = 18531244

// 함수 구현체 
object Func {
  // line의 길이를 반환하는 함수 
  def mapFunc(line: String): Int = { line.length }
  // a, b의 합을 반환하는 함수 
  def reduceFunc(a:Int, b:Int): Int = { a + b }
}

// RDD에 mapFunc, reduceFunc를 전달
scala> cctvRDD.map(Func.mapFunc).reduce(Func.reduceFunc)
res11: Int = 18531244           
```





---





### 캐쉬 이용

RDD는 처리 결과를 메모리나 디스크에 저장하고 다음 계산에 이용할 수 있습니다. 반복작업의 경우 이 캐쉬를 이용해서 처리 속도를 높일 수 있습니다. 하지만 단일작업의 경우 데이터 복사를 위한 오버헤드가 발생하여 처리시간이 더 느려질 수 있습니다. 따라서 작업의 종류와 영향을 파악한 후에 캐슁을 이용하는 것이 좋습니다.

RDD는 `persist()`, `cache()` 메소드를 이용하여 캐슁을 지원합니다. 캐슁한 데이터에 문제가 생기면 자동으로 복구합니다. 또한 저장 방법을 설정할 수 있어서, 메모리나 디스크에 저장 할 수도 있습니다. 



| 설정            | 설명                                                         |
| :-------------- | :----------------------------------------------------------- |
| MEMORY_ONLY     | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부만 저장하고 필요할 때마다 계산. 기본값 |
| MEMORY_AND_DISK | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부는 메모리, 일부는 디스크에 저장 |
| DISK_ONLY       | RDD를 디스크에 저장                                          |



```scala
val txts = sc.textFile("/user/sample.txt")
val pairs = txts.flatMap(line => line.split(" ")).map(word => (word, 1))

// 각 단계의 결과를 캐슁 
scala> pairs.persist()
res39: pairs.type = MapPartitionsRDD[36] at map at <console>:26

val counts = pairs.reduceByKey(_ + _) 
scala> counts.persist()
res38: counts.type = ShuffledRDD[37] at reduceByKey at <console>:28
```



---





## 복잡한 RDD 연산



### key, value를 이용한 처리

---

스파크는 맵리듀스 처럼 (키, 밸류) 쌍을 이용한 처리도 가능합니다. 기본적으로 제공하는 `flatmap`, `reduceByKey`,  `groupByKey`, `mapvalues`, `sortByKey`를 이용해서 좀 더 편리한 처리가 가능합니다.

다음의 워크 카운트는 키, 밸류를 이용한 처리를 확인할 수 있습니다. 파일의 데이터를 읽어서 `flatmap`를 이용하여 단어별로 분리하고, `map`을 이용하여 단어의 개수를 세어줍니다. `reduceByKey`를 이용하여 단어별로 그룹화 하여 단어가 나타난 개수를 세어줍니다.

```scala
val txts = sc.textFile("/user/sample")
val pairs = txts.flatmap(line => line.split(" ")).map(word => (word, 1))
val counts = pairs.reduceByKey(_ + _)

scala> counts.take(10).foreach(println)
(under,1)                                                                       
(better.,1)
(goals,1)
(call,3)
(its,7)
(opening,1)
(extraordinary,1)
(internationalism，to,1)
(have,4)
(include,2)
```



---



### 브로드캐스트(broadcast)

---

브로드 캐스트는 맵리듀스의 디스트리뷰트 캐쉬(distribute cache)와 유사한 역활을 하는 모든 노드에서 공유되는 읽기 전용 값입니다. `broadcast()` 이용하여 사용할 수 있습니다. 조인에 이용되는 값들을 선언하여 이용할 수 있습니다.

다음의 예제에서 `broadcastVar` 변수는 클러스터의 모든 노드에서 사용할 수 있는 값이 됩니다.

```scala
scala> val broadcastVar = sc.broadcast(Array(1, 2, 3))
broadcastVar: org.apache.spark.broadcast.Broadcast[Array[Int]] = Broadcast(0)

scala> broadcastVar.value
res0: Array[Int] = Array(1, 2, 3)
```





### 셔플

---

스파크에서 조인, 정렬 작업은 셔플(Shuffle) 작업을 실행합니다. 셔플은 파티션간에 그룹화된 데이터를 배포하는 메커니즘입니다. 셔플은 임시 파일의 복사, 이동이 있기 대문에 많은 비용이 들게 됩니다. 