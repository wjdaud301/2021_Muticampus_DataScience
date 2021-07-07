#########  원형리스트  #########

## 함수 선언부 ##

def isQueueEmpty():
    global SIZE, queue, front, rear
    if front == rear:
        return True
    else:
        return False

def isQueueFull():
    global SIZE, queue, front, rear
    if (rear+1)%SIZE == front :
        return True
    else:
        return False

def enQueue(data):
    global SIZE, queue, front, rear
    if isQueueFull():
        print('queue full!!')
        return
    rear = (rear+1) % SIZE
    queue[rear] = data

def deQueue():
    global SIZE, queue, front, rear
    if isQueueEmpty():
        print('queue empty!!')
        return None
    front = (front+1) % SIZE
    data = queue[front]
    queue[front] = None
    return data

def peek():
    global SIZE, queue, front, rear
    if isQueueEmpty:
        print('queue empty!!')
        return None
    return queue[(front+1)%SIZE]

## 전역 변수부 ##
SIZE = 5
queue = [None for _ in range(SIZE)]
front = rear = 0


## 메인 코드부 ##
if __name__=='__main__':
    select = input('E:추출, I:삽입, V:확인, X:종료 --> ')
    
    while select !='X' and select != 'x' :
        if select =="I" or select == 'i':
            data = input('추가할 데이터 -->')
            enQueue(data)
            print('큐 상태 : ',queue)
            print("front : ",front,", rear : ",rear)

        elif select == 'E' or select == 'e':
            data = deQueue()
            print('추출된 데이터 --> ', data)
            print('큐 상태 : ',queue)
            print("front : ",front,", rear : ",rear)
            
        elif select == 'V' or select == 'v':
            data = peek()
            print('확인된 데이터 --> ', data)
            print('큐 상태 : ',queue)
            print("front : ",front,", rear : ",rear)
            
        else:
            print("입력이 잘못됨")
        
        select = input('E:추출, I:삽입, V:확인, X:종료 --> ')
    print("프로그램 종료!")