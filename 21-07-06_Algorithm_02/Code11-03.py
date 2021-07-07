#### 선택정렬의 최종버전 ####
def selectionSort(ary):
    n = len(ary)
    for i in range(n-1): # 사이클(큰 반복 3회)
        maxIdx = i
        for k in range(i+1,n): # 작은 반복
            if ary[minIdx] > ary[k]:
                minIdx = k
        ary[i], ary[minIdx] = ary[minIdx], ary[i]
    return ary 



## 전역 변수부 ##
import random
dataAry = [random.randint(50,190) for _ in range(8)]


## 메인 코드부 ##
print('정렬전 --> ', dataAry)

dataAry = selectionSort(dataAry)

print('정렬후 --> ', dataAry)
