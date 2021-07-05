
katoc = []
select = 0

def add_data(friend):
    katoc.append(None)
    klen = len(katoc)
    katoc[klen-1] = friend


def insert_data(position, friend):
    katoc.append(None)
    klen = len(katoc)

    for i in range(klen-1,position,-1):
        katoc[i] = katoc[i-1]
        katoc[i-1] =None
    katoc[position] = friend

def delete_data(position):
    klen = len(katoc)
    katoc[position] = None
    for i in range(position+1,klen):
        katoc[i-1] = katoc[i]
        katoc[i] = None
    del katoc[klen-1]


while select !=4 :
    select = int(input('1:추가, 2:삽입, 3:삭제, 4:종료 --> '))

    if select ==1:
        data = input('추가할 데이터 -->')
        add_data(data)
        print(katoc)

    elif select ==2:
        data = input('추가할 데이터 --> ')
        pos =int(input('위치를 입력해주세요 --> '))
        insert_data(pos,data)
        print(katoc)

    elif select ==3:
        pos = int(input('삭제할 데이터 위치를 입력해주세요 -->'))
        delete_data(pos)
        print(katoc)
        
    elif select ==4:
        print(katoc)
        break

    else:
        print("1~4중에 하나를 입력하세요")