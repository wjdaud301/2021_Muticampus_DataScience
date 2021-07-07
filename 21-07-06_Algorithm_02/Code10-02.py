########### 재귀 함수 ###########

def openBox():
    global count
    print("박스 열기 ~~")
    count  -= 1
    if count == 0:
        print("### 반지 넣기 ###")
        return
    openBox()
    print("박스 닫기 !!")


def addNumber(num):
    if num <= 1:
        return 1
    return num + addNumber(num-1)
    


count = 10
# openBox()
print(addNumber(5))