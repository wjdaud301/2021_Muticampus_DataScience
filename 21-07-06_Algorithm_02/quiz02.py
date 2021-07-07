##### quiz01 문제를 list하나로 만들기 ######

def findMinIdx(ary):
    for i in range(len(ary)-1):
        maxIdx = i
        for j in range(i+1,len(ary)):
            if ary[maxIdx] < ary[j]:
                maxIdx = j
        ary[maxIdx], ary[i] = ary[i], ary[maxIdx]
    return ary



## 전역변수부 ##
import random
dataAry = [random.randint(44032,55203) for _ in range(30)]


## 메인 코드부 ##
print('정렬전 --> ', list(map(chr,dataAry)))

dataAry = findMinIdx(dataAry)

print('정렬후 --> ', list(map(chr,dataAry)))

'''
정렬전 -->  ['륗', '퐫', '뭙', '젅', '괶', '겿', '껫', '죘', '볩','뉰', 
            '닌', '설', '쯉', '둭', '럙', '뚫', '념', '듚', '뙆', '뤓',
            '뿸', '옡', '릙', '딩', '섴', '쬽', '먂', '돋', '햒', '딞']


정렬후 -->  ['햒', '퐫', '쯉', '쬽', '죘', '젅', '옡', '섴', '설', '뿸', '볩',
            '뭙', '먂', '릙', '륗', '뤓', '럙', '뚫', '뙆', '딩', '딞', '듚',
            '둭', '돋', '닌', '뉰', '념', '껫', '괶', '겿']
'''