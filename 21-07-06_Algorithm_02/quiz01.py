#### 한글 배열을 30글자 만들고, 내림차순으로 정렬하기 ####
def findMinIdx(ary):
    minIdx = 0
    for i in range(1,len(ary)):
        if ary[minIdx] < ary[i]:
            minIdx = i
    return minIdx


## 전역변수부 ##
import random
before = [random.randint(44032,55203) for _ in range(30)]
after = []


## 메인 코드부 ##
print('정렬전 --> ', list(map(chr,before)))

for _ in range(len(before)):
    minPos = findMinIdx(before)
    after.append(chr(before[minPos]))
    del before[minPos]

print('정렬후 --> ', after)

'''
정렬전 -->  ['륗', '퐫', '뭙', '젅', '괶', '겿', '껫', '죘', '볩','뉰', 
            '닌', '설', '쯉', '둭', '럙', '뚫', '념', '듚', '뙆', '뤓',
            '뿸', '옡', '릙', '딩', '섴', '쬽', '먂', '돋', '햒', '딞']


정렬후 -->  ['햒', '퐫', '쯉', '쬽', '죘', '젅', '옡', '섴', '설', '뿸', '볩',
            '뭙', '먂', '릙', '륗', '뤓', '럙', '뚫', '뙆', '딩', '딞', '듚',
            '둭', '돋', '닌', '뉰', '념', '껫', '괶', '겿']
'''