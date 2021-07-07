## 클래스 함수부 ##

class Node():
    def __init__(self) -> None:
        self.data = None
        self.link = None

def printNode(node):
    current = node
    print(current.data, end=' ')
    while current.link != None :
        current = current.link
        print(current.data, end=' ')
    print()


## 전역 변수 부 ##
import random
memory = []
head, pre, current =None, None, None
dataArray = [random.randint(1000,9999) for i in range(20)]

## 메인 부 ##
if __name__ == '__main__':
    # node 생성
    node = Node()
    # head가 node를 가르키게 설정
    head = node
    # data 첫번째를 노드의 data로 삽입
    node.data = dataArray[0]
    # memory 공간에 삽입
    memory.append(node)

    for i in dataArray[1:]:
        # 현재노드를 이전노드로 할당
        pre = node
        # 현재 노드 생성
        node = Node()
        # 현재 노드의 data할당
        node.data = i
        # 이전 노드의 link를 현재 노드를 가르키도록 설정
        pre.link = node
    
    printNode(head)
