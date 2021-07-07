
############ 이진 탐색 트리 ###########

class TreeNode():
    def __init__(self) -> None:
        self.left = None
        self.data = None
        self.right = None


## 전역 변수
memory=[]
root = None
# 데이터베이스 또는 크롤링으로 얻은 rowdata 집합
nameAry= ['블랙핑크','레드벨벳','에이핑크','걸스데이','트와이스','마마무']

# 첫번째 노드 생성
name = nameAry[0]
node = TreeNode()
node.data = name
# node를 root로 할당
root = node
# memory 삽입
memory.append(node)

for name in nameAry[1:]:    
    node = TreeNode()  # 노드 생성
    node.data=name
    current = root     # currrent를 현재 root로 설정 

    while True:
        if name < current.data :  # 만약 값이 root의 data보다 작을경우
            if current.left == None: # root의 왼쪽노드가 없을 경우
                current.left = node
                break
            current = current.left   # 있다면 root노드에서 왼쪽노드로 current 옮긴다
        else :                     # 만약 값이 root의 data보다 클 경우
            if current.right == None: # root의 오른쪽 노드가 없을 경우
                current.right = node
                break
            current = current.right   # 있다면 root노드에서 오른졲노드로 current 옮긴다
    
    memory.append(node)  # memory의 저장


## 데이터 검색 ##
findName = '마마무'
current = root
while True:
    if findName == current.data :
        print(findName, '를 찾았습니다.')
        break
    elif findName < current.data :
        if current.left == None:
            print('없습니다.')
            break
        current = current.left
    else:
        if current.right == None:
            print('없습니다.')
            break
        current = current.right

