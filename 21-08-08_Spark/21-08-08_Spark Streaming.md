## 1. 디스트림 (DStream)

스파크 스트리밍은 실시간 데이터 분석을 위한 스파크 컴포넌트 입니다. 데이터는 카프카, 플럼, 키네시스, TCP 소켓등 다양한 경로를 통해서 입력 받고, `map`, `reduce`, `window`등의 연산을 통해 데이터를 분석하여 최종적으로 파일시스템, 데이터베이스 등에 적재 됩니다.
또한 이 데이터를 스파크의 머신러닝(MLib), 그래프 컴포넌트(GraghX)에 이용할 수도 있습니다.

스파크 스트리밍은 실시간 데이터 스트림을 받아서 데이터를 디스트림(DStream, distretized stream, 이산 스트림)이라 불리는 추상화 개념의 작은 배치 단위로 나누고 디스트림을 스파크 엔진으로 분석합니다.



### 디스트림 

---

디스트림은 시간별로 도착한 데이터들의 연속적인 모임입니다. 각 디스트림은 시간별 RDD들의 집합으로 구성됩니다. 플럼, 카프카, HDFS등 다양한 원천으로 부터 디스트림을 입력 받을 수 있습니다.

디스트림은 RDD와 마찬가지로 두 가지 타입의 연산을 제공합니다. 하나는 **새로운 디스트림을 만들어 낼 수 있는** **트랜스포메이션** 연산이고, 하나는 **외부 시스템에 데이터를 써주는 출력 연산**이다. 시간 관련이나 슬라이딩 윈도우 같은 실시간 분석을 위한 특별한 기능도 지원합니다.





---





## 2. 스트리밍 컨텍스트 초기화

디스트림(DStream)은 Streaming context를 이용하여 생성합니다. Streaming Context는 Spark config 객체나Spark context 객체를 이용하여 초기화 할 수 있습니다.

Streaming context 를 초기화 할 때는 DStream의 처리 간격을 지정해야 합니다.  DStream의 처리 간격이 Stream의 배치 단위가 됩니다.



### Spark Config

---

Spark config를 이용하는 방법은 다음과 같이 Spark Context나 Spark session을 초기화할 때와 동일합니다.
Spark Config에 설정 정보를 입력하고 이를 이용해서 초기화합니다.

```scala
import org.apache.spark._
import org.apache.spark.streaming._

val conf = new SparkConf().setMaster("yarn").setAppName("NetworkWordCount")
val ssc = new StreamingContext(conf, Seconds(1))    // 1초간격 배치 처리 
```





### Spark Context

---

이미 스파크 컨텍스트 객체가 생성되어 있는경우, 스파크 컨피그를 이용하지 않고 스파크 컨텍스트를 전달하는 방법으로 초기화 할 수 있습니다. **스파크 쉘**에서 스트리밍 컨텍스트를 이용할 때 사용할 수 있습니다.

```scala
import org.apache.spark._
import org.apache.spark.streaming._

// sc는 생성된 스파크 컨텍스트 객체 
val ssc = new StreamingContext(sc, Seconds(5))      // 5초간격 배치 처리 
```



---







## 3. 스트리밍 워드 카운트 예제



### 스트리밍 워드 카운트

---

스트리밍 컨텍스트를 초기화 할 때 `Seconds(5)`를 전달하여 DStream 처리 간격을 5초로 설정

`socketTextstream`을 이용해서 텍스트 데이터를 전달한 IP, port에 접속하여 입력 받습니다. 이 데이터를 워드 카운트 처리하고 `print`를 이용하여 화면에 출력합니다.

`start`를 호출하면 소켓 텍스트 스트림을 이용하여 원격지에 접속하여 텍스트 스트림을 입력 받습니다.
`awaitTermination`을 이용하면 별도의 스레드로 작업을 시작하여 사용자의 세션이 끊어져도 작업을 진행합니다.

```scala
import org.apache.spark._
import org.apache.spark.streaming._

val ssc = new StreamingContext(sc, Seconds(5))      // 5초간격 배치 처리 
val lines = ssc.socketTextStream("127.0.0.1", 9999) // 텍스트를 입력 받을 IP, port 입력 
val words = lines.flatMap(_.split(" "))
val pairs = words.map(word => (word, 1))
val wordCounts = pairs.reduceByKey(_ + _)
wordCounts.print()

ssc.start()             // 데이터 받기 시작 
ssc.awaitTermination()      // 별도의 스레드로 작업 시작 
```



### 실행

이 예제의 실행은 로그 데이터 전달을 위한 서버(netcat)와 클라이언트(스파크 스트리밍)를 실행하는 것으로 나눌 수 있습니다. 서버는 넷캣(netcat, nc)을 이용합니다.





#### netcat 실행

`nc`명령을 다음과 같이 입력하면 9999 포트에서 TCP입력을 대기합니다. 연결되면 사용자 입력을 전달합니다.

```
# 9999 포트를 열어서 대기(listen)
$ nc -l 9999
a b c d a b c d a a a
```





#### 스파크 스트리밍 실행

스파크 스트리밍은 위의 예제를 스파크 서브밋(spark-submit)을 이용하여 제출해도 되고, 스파크 쉘(spark-shell)을 이용하여 실행해도 됩니다. 스파크 서브밋을 이용하는 경우 위 예제를 입력하고 `start`를 호출하면 원격지에 접속하여 데이터를 전달 받고, 워드카운트를 처리하여 데이터를 출력합니다.

```
scala> ssc.start()    // 데이터 받기 시작 
-------------------------------------------
Time: 1548652935000 ms
-------------------------------------------
(d,2)
(b,2)
(a,5)
(c,2)
```

위와 같이 입력된 데이터를 시간 배치 간격으로 처리하여 출력합니다





---





## 4. DStream 연산



### 조인, 유니온 연산

---

스트림의 조인과 유니온 연산도 쉽게 처리할 수 있습니다. 스트림끼리의 연산은 `join`, `leftOuterJoin`, `rightOuterJoin`, `fullOuterJoin`, `union` 연산을 이용해서 처리할 수 있습니다.



#### 디스트림간의 연산

```scala
ㅍval stream1: DStream[String, String] = ...
val stream2: DStream[String, String] = ...
val joinedStream = stream1.join(stream2)
```

조인의 윈도우 연산도 쉽게 처리할 수 있습니다. 다음과 같이 `window`를 이용하여 시간간격을 입력하면 됩니다.

```
val windowedStream1 = stream1.window(Seconds(20))
val windowedStream2 = stream2.window(Minutes(1))
val joinedStream = windowedStream1.join(windowedStream2)
```



#### 조인 연산 예제

```scala
import org.apache.spark._
import org.apache.spark.streaming._

val ssc = new StreamingContext(sc, Seconds(5))
val lines1 = ssc.socketTextStream("1.1.1.1", 9999)
val wordCounts1 = lines1.flatMap(_.split(" ")).map(word => (word, 1)).reduceByKey(_ + _)

val lines2 = ssc.socketTextStream("1.1.1.1", 9998)
val wordCounts2 = lines2.flatMap(_.split(" ")).map(word => (word, 1)).reduceByKey(_ + _)

val unionStream = wordCounts1.union(wordCounts2)
unionStream.print()

ssc.start()
```





### RDD와 디스트림간 연산

RDD와 디스트림간의 연산도 `transform`을 이용해서 처리 가능합니다.

```scala
val dataset: RDD[String, String] = ...
val windowedStream = stream.window(Seconds(20))...
val joinedStream = windowedStream.transform { rdd => rdd.join(dataset) }
```





### 출력 연산

디스트림 연산의 결과는 출력 연산(Output Operation)을 이용해서 파일시스템이나 데이터베이스에 외부 저장소에 저장할 수 있습니다.

| 함수                                    | 비고                                                         |
| :-------------------------------------- | :----------------------------------------------------------- |
| print()                                 | 디스트림 배치의 데이터에서 10개를 출력. 디버그용             |
| saveAsTextFiles(*prefix*, [*suffix*])   | 디스트림 배치의 데이터를 텍스트 파일로 저장. 파일 명은 prefix-TIME_IN_MS[.suffix]로 저장 |
| saveAsObjectFiles(*prefix*, [*suffix*]) | 디스트림 배치의 데이터를 시퀀스 파일로 저장.                 |
| saveAsHadoopFiles(*prefix*, [*suffix*]) | 디스트림 배치의 데이터를 하둡 파일로 저장                    |
| foreachRDD(func)                        | 디스트림에 함수를 적용하여 RDD를 생성하고 이를 출력하는 범용적인 출력 연산. 주어진 함수는 외부 시스템에 데이터를 쓰는 함수. |





### 파일 저장

파일을 저장하는 함수는 저장할 디렉토리와 접미어를 파라미터로 받습니다. 각 배치의 결과는 주어진 디렉토리아래 저장되고 저장시간과 접미어가 폴더명으로 생성됩니다.

```
wordCounts.saveAsTextFiles("/user/stream/txt_data", "txt")
```

파일로 저장하면 다음과 같이 주어진 폴더명으로 디렉토리를 생성하고 시간대별로 폴더를 생성하여 데이터를 저장합니다.

```scala
$ hadoop fs -ls -R /user/shs/stream/
drwxr-xr-x   - hadoop hadoop          0 2019-01-29 10:21 /user/shs/stream/txt_data-1548757278000.txt
-rw-r--r--   2 hadoop hadoop          0 2019-01-29 10:21 /user/shs/stream/txt_data-1548757278000.txt/_SUCCESS
-rw-r--r--   2 hadoop hadoop         12 2019-01-29 10:21 /user/shs/stream/txt_data-1548757278000.txt/part-00000
-rw-r--r--   2 hadoop hadoop         12 2019-01-29 10:21 /user/shs/stream/txt_data-1548757278000.txt/part-00001
drwxr-xr-x   - hadoop hadoop          0 2019-01-29 10:21 /user/shs/stream/txt_data-1548757281000.txt
```







### foreachRDD를 이용한 범용 연산

`foreachRDD`를 이용한 연산은 RDD의 모든 연산을 사용할 수 있습니다. 이를 이용해서 외부 DB에 데이터를 저장할 수 있습니다.

```scala
dstream.foreachRDD { rdd =>
  val connection = createNewConnection()  // executed at the driver
  rdd.foreach { record =>
    connection.send(record) // executed at the worker
  }
}
```