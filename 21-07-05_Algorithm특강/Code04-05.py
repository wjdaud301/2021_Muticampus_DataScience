## 클래스 또는 선언부 ##
class Node():
    def __init__(self) -> None:
        self.data = None
        self.link = None


def printNodes(start):
    current = start
    print(current.data, end=' ')
    while current.link != None :
        current = current.link
        print(current.data, end=' ')
    print()

def insertNode(findData, insertData) :
    global head, pre, current, memory

    if head.data == findData:
        node = Node()
        node.data = insertData
        node.link = head
        head = node
        return
    
    current = head
    while current.link != None:
        pre = current
        current = current.link
        if current.data == findData:
            node = Node()
            node.data = insertData
            node.link = current
            pre.link = node
            return
    
    node = Node()
    node.data = insertData
    current.link = node

def deleteNode(deleteData):
    global head, pre, current, memory

    if head.data == deleteData:
        current = head
        head = head.link
        del(current)
        return
    
    current = head
    while current.link != None:
        pre = current
        current = current.link
        if current.data == deleteData:
            pre.link = current.link
            del(current)
            return



## 전역 변수 부 ##
memory = []
head, pre, current = None, None, None
dataArray=['다현','정연','쯔위','사나','지효'] # DB, Datacrawling...


## 메일 코드부 ##
if __name__=='__main__': # C, Java, C++, C# ==> main()함수
    
    node = Node()
    node.data = dataArray[0]
    head = node
    memory.append(node)

    for data in dataArray[1:]: #'정연','쯔위','사나','지효'
        pre = node
        node = Node() 
        node.data = data # 정연, 쯔위...
        pre.link = node
        memory.append(node)

    printNodes(head)
