## 1. Kafka 란?

Kafka는 `Pub-Sub`모델의 `메시지 큐` 입니다. 분산환경에 특화되어 있는 특징을 가지고 있다.





## 2. 구성요소



### 2.1 Event

`Event`는 kafka에서 Producer와 Consumer가 데이터를 주고 받는 단위



### 2.2 Producer

`Producer`는 kafka에 이벤트를 게시(Post)하는 클라이언트 어플리케이션



### 2.3 Consumer

`Consumer`는 이러한 Topic을 구독하고 이로부터 얻어낸 이벤트를 처리하는 클라이언트 어플리케이션



### 2.4 Topic

이벤트가 쓰이는 곳, Producer는 이 Topic에 이벤트를 게시하고 Consumer는 Topic으로 부터 이벤트를 가져와 처리한다. Topic은 파일시스템의 폴더와 유사하며, 이벤트는 폴더안의 파일과 유사하다.

Topic에 저장된 이벤트는 필요한 만큼 다시 읽을 수 있다.



### 2.5 Partition

Topic은 여러 Broker에 분산되어 저장되며, 이렇게 분산된 Topic을 `partition`이라고 한다.

어떤 이벤트가 Partition에 저장될지는 이벤트의 `key`에 의해 정해지며, 같은 키를 가지는 이벤트는 항상 같은 Partition에 저장된다.

kafka는 Topic의 Partition에 지정된 `Consumer`가 항상 정확히 동일한 순서로 Partition의 이벤트를 읽을 것을 보장한다.







## 3. Kafka의 주요 개념



### 3.1 Producer와 Consumer의 분리

kafka의 Producer와 Consumer는 완전 별개로 동작을 한다.

Producer는 Broker의 Topic에 메시지를 게시하기만 하면, Consumer는 Broker의 특정 Topic에서 메시지를 가져와 처리를 하기만 한다.





### 3.2 Push와 Pull 모델

kafka의 `Consumer`는 `pull`모델을 기반으로 메시지 처리를 진행한다. 즉, Broker가 Consumer에게 메시지를 전달하는 것이 아닌, Consumer가 필요할 때, Broker로 부터 메시지를 가져와 처리하는 형태이다.





### 3.3 소비된 메시지 추적 (Commit과 Offset)

Consumer의 `pull()`은 이전에 `commit한 offset`이 존재하면, 해당 offset 이후의 메시지를 읽어오게 됩니다. 또 읽어온 뒤, 마지막 offset을 commit한다. 이어서 pull()이 실행되면 방금 전 commit한 offset 이후의 메시지를 읽어와 처리하게 된다.





### 3.4 메시지(이벤트) 전달 컨셉

kafka는 메시지 전달을 할 때 보장하는 여러가지 방식이 있다.

- At most once(최대 한번)

메시지가 손실될 수 있지만, 재전달은 하지 않는다.



- At least once(최소 한번)

메시지가 손실되지 않지만, 재전달이 일어난다.



- Exactly once(정확히 한번)

메시지는 정확히 한번 전달이 된다.