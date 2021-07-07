def findMinIdx(ary):
    minIdx = 0
    for i in range(1,len(ary)):
        if ary[minIdx] > ary[i]:
            minIdx = i
    return minIdx


## 전역변수부 ##
import random
before = [random.randint(50,190) for _ in range(8)]
after = []

## 메인 코드부 ##
print('정렬전 --> ', before)

for _ in range(len(before)):
    minPos = findMinIdx(before)
    after.append(before[minPos])
    del before[minPos]

print('정렬후 --> ', after)
