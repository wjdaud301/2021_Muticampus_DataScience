![2](21-06-10_정리.assets/2.PNG)



![1](21-06-10_정리.assets/1.PNG)



---





## 1. 데이터 준비 과정의 중요성

데이터 분석에 드는 노력의 80% , 어쩌면 그 이상은 모델링이 아닌 데이터의 특성을 파악하는 EDA, missing value를 처리하는 등의 정제 작업을 진행하는 데이터 전처리, 좋은 모델링을 위해 적절한 feature를 선택하는 feature selection의 데이터 그 자체의 특성을 파악하고 이를 정제하는데 소요된다


데이터 준비 과정은 원시 데이터를 모델링에 적합한 형식으로 변환하는 작업이 중심 내용이며, 데이터 를 준비하는 것은 예측 모델 생성 프로젝트에서 가장 중요한 부분이며 가장 많은 시간이 소요된다.

모든 데이터 준비 과정은 기계 학습 알고리즘에 맞추어져 진행 되며, 실제 데이터와 매개 변수 등을 활용한다. 실질적인 데이터 준비 과정에는 <u>**데이터 정리, 특징 추출, 데이터 변환, 차원 축소**</u> 등에 대한 지식이 필요하다.

예측 모델링 프로젝트에는 데이터로부터 학습이 진행됩니다. 데이터는 해결하려는 문제를 특징 짓는 도메인으로 부터 경험 할 수 있는 사례를 제공하지만, 분류 또는 회귀와 같은 예측 모델링 프로젝트에 서 **원시 데이터는 일반적으로 직접 사용할 수 없습니다**. 

이것이 사실인 네 가지 주요 이유가 있습니다. 원시 데이터는 기계 학습 모델을 맞추고 평가하는 데 사용되기 전에 사전 처리 되어야 합니다. 기계 학습 프로젝트의 데이터 준비 단계에서 사용하거나 탐색 할 수 있는 일반 또는 표준 작업이 있습니다. 

* **데이터 정리** : 데이터의 오류 또는 오류를 식별하고 수정 
* **특징 선택** : 작업과 가장 관련된 입력 변수 식별 
* **데이터 변환** : 변수의 척도 또는 분포 파악 
* **특징 엔지니어링** : 사용 가능한 데이터에서 새로운 변수 도출 
* **차원 감소** : 데이터의 간결한 예측 생성





---





## 2. 결측치의 처리방법



실제 데이터에는 종종 결측값이 있습니다. 데이터에는 기록되지 않은 관찰 및 데이터 손상과 같은 여 러 가지 이유로 인해 누락 된 값이 있을 수 있습니다. 누락 된 데이터 처리가 중요합니다. 

많은 기계 학습 알고리즘이 결측값이 있는 데이터를 지원하지 않기 때문입니다. 누락 된 값을 데이터 로 채우는 것을 <u>**데이터 대치**</u>라고 하며 데이터 대치에 대한 일반적인 접근 방식은 

**각 열 (예 : 평균)에 대한 통계 값을 계산하고 해당 열의 모든 누락 된 값을 통계로 바꾸는 것**입니다



* SimpleImputer() **클래스**를 사용하여 NaN 값으로 표시된 모든 누락 된 값을 열의 평균으로 변환 할 수 있습니다.

SimpleImputer( strategy = ' ')

```
strategy Option
	'mean': 평균값 (default)    
	'median': 중앙값    
	'most_frequent': 최빈값   
	'constant': 특정값,  예 SimpleImputer(strategy='constant', fill_value=1)
```

* #### 2-1 기본예제

```python
import numpy as np 
import pandas as pd 
from sklearn.impute import SimpleImputer 

##########데이터 로드

df = pd.DataFrame([
    [2, 1, 3],
    [3, 2, 5],
    [3, np.nan, 7],
    [5, np.nan, 10],
    [7, 5, 12],
    [2, 5, 7],
    [8, 9, 13],
    [9, 10, 13],
    [6, 12, 12],
    [9, 2, 13],
    [6, 10, 12],
    [2, 4, 6]
], columns=['hour', 'attendance', 'score'])

##########데이터 분석

df.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 12 entries, 0 to 11
Data columns (total 3 columns):
 #   Column      Non-Null Count  Dtype  
---  ------      --------------  -----  
 0   hour        12 non-null     int64  
 1   attendance  10 non-null     float64
 2   score       12 non-null     int64  
dtypes: float64(1), int64(2)
memory usage: 416.0 bytes
'''
print(df.isnull().sum())
'''
hour          0
attendance    2
score         0
dtype: int64
'''

##########데이터 전처리
# score columns를 y축으로 할당하고 나머지를 x축으로 할당한다
x_data = df.drop(['score'], axis=1) 
y_data = df['score']

# transformer변수로 simpleImpuper()클래스 객체생성
transformer = SimpleImputer()

# x_data에 결측치가 발견되고 simpleImputer()인자가 default이기 때문에 평균값으로 대치
transformer.fit(x_data)
x_data = transformer.transform(x_data)
print(x_data)
'''
[[ 2.  1.]
 [ 3.  2.]
 [ 3.  6.]
 [ 5.  6.]
 [ 7.  5.]
 [ 2.  5.]
 [ 8.  9.]
 [ 9. 10.]
 [ 6. 12.]
 [ 9.  2.]
 [ 6. 10.]
 [ 2.  4.]]
'''
```

참고) fit_transform() 함수 사용

```python
x_data = transformer.fit_transform(x_data)
```



참고) 데이터가 학습 데이터와 테스트 데이터로 나누어 진 경우는 반드시 fit() 함수와 transform() 함수를 따로 사용

```python
transformer.fit(x_train) #SimpleImputer 모델에 x_train 데이터 적용 (평균값 계산)
x_train = transformer.transform(x_train) 
x_test = transformer.transform(x_test)
```





* #### 2-2 수업예제

```python
# statistical imputation transform for the horse colic dataset
from numpy import isnan
from pandas import read_csv
from sklearn.impute import SimpleImputer

# load dataset
url = 'https://raw.githubusercontent.com/jbrownlee/Datasets/master/horse-colic.csv'
dataframe = read_csv(url, header=None, na_values='?')

# split into input and output elements
data = dataframe.values
ix = [i for i in range(data.shape[1]) if i != 23]
X, y = data[:, ix], data[:, 23]

# print total missing
print('Missing: %d' % sum(isnan(X).flatten()))
```
```
출력 결과 :
    Missing: 1605
```
```python
# define imputer(결측치제거)
imputer = SimpleImputer(strategy='mean')

# fit on the dataset
imputer.fit(X)

# transform the dataset
Xtrans = imputer.transform(X)

# print total missing
print('Missing: %d' % sum(isnan(Xtrans).flatten()))
```
```python
출력 결과 :
    Missing: 0
```





---







## 3. 특징추출

우리는 **모델의 정확도 혹은 속도 등을 위해 모든 feature를 사용하는 것이 아닌 학습에 필요한 적절한 feature만을 선택**해야 할 것이다. 이렇게 적절한 feature를 선택하는 과정을 **feature selection**이라고 한다. 



* ### RFE 

 RFE(Recursive Feature Elimination)는 어떤 관점에서 바라 보면 feature selection의 가장 단순한 방법이다. **모든 feature들로부터 feature를 하나하나 제거하면서 원하는 개수의 feature가 남을 때까지 이를 반복**한다. 

즉, 학습하고 싶은 모델을 정하고, 이 모델로 모든 feature를 활용하여 데이터를 학습했을 때(full model)의 각 feature의 feature importance를 도출한다. 그리고 feature importance가 낮은 feature부터 하나씩 제거해가면서 원하는 feature 개수가 될 때까지 이를 반복하는 것이다. 이렇게 원하는 feature 개수에 해당하는 상위 feature importance를 가지는 feature들이 최종 feature selection 결과가 된다.



* #### 3-1 기본예제

##### report which features were selected by RFE (특징 추출)


```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier

# define dataset
X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, n_redundant=5, random_state=1)

X.shape
출력 : (1000, 10)

y.shape
출력 : (1000,)


####### 10개의 feature 중  5개 선택 #########

# define RFE
rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=5)

# fit RFE
rfe.fit(X, y)

# summarize all features
for i in range(X.shape[1]):
  print('Column: %d, Selected=%s, Rank: %d' % (i, rfe.support_[i], rfe.ranking_[i]))

출력 :
Column: 0, Selected=False, Rank: 4
Column: 1, Selected=False, Rank: 5
Column: 2, Selected=True, Rank: 1
Column: 3, Selected=True, Rank: 1
Column: 4, Selected=True, Rank: 1
Column: 5, Selected=False, Rank: 6
Column: 6, Selected=True, Rank: 1
Column: 7, Selected=False, Rank: 2
Column: 8, Selected=True, Rank: 1
Column: 9, Selected=False, Rank: 3
```





* #### 3-2 실습예제

##### credit_cards_dataset.csv 데이터에서 feature 10개 추출하기


```python
from sklearn.datasets import make_classification
from sklearn.feature_selection import RFE
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# define dataset
data = pd.read_csv("../Big_Data_Analysis/feature_selection/credit_cards_dataset.csv")
data = data.rename(columns={'default.payment.next.month': 'DEFAULT_NEXT_MONTH'})

x_data = data.drop(['DEFAULT_NEXT_MONTH'],axis=1)
y_data = data['DEFAULT_NEXT_MONTH']
x_data = x_data.drop(['ID'],axis=1)

x_data.shape
    출력 : (30000, 23)

x_data.info()
    출력 :
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 30000 entries, 0 to 29999
    Data columns (total 23 columns):
     #   Column     Non-Null Count  Dtype  
    ---  ------     --------------  -----  
     0   LIMIT_BAL  30000 non-null  float64
     1   SEX        30000 non-null  int64  
     2   EDUCATION  30000 non-null  int64  
     3   MARRIAGE   30000 non-null  int64  
     4   AGE        30000 non-null  int64  
     5   PAY_0      30000 non-null  int64  
     6   PAY_2      30000 non-null  int64  
     7   PAY_3      30000 non-null  int64  
     8   PAY_4      30000 non-null  int64  
     9   PAY_5      30000 non-null  int64  
     10  PAY_6      30000 non-null  int64  
     11  BILL_AMT1  30000 non-null  float64
     12  BILL_AMT2  30000 non-null  float64
     13  BILL_AMT3  30000 non-null  float64
     14  BILL_AMT4  30000 non-null  float64
     15  BILL_AMT5  30000 non-null  float64
     16  BILL_AMT6  30000 non-null  float64
     17  PAY_AMT1   30000 non-null  float64
     18  PAY_AMT2   30000 non-null  float64
     19  PAY_AMT3   30000 non-null  float64
     20  PAY_AMT4   30000 non-null  float64
     21  PAY_AMT5   30000 non-null  float64
     22  PAY_AMT6   30000 non-null  float64
    dtypes: float64(13), int64(10)
    memory usage: 5.3 MB


y_data.shape
    출력 : (30000,)

y_data
    출력 :
    0        1
    1        1
    2        0
    3        0
    4        0
            ..
    29995    0
    29996    0
    29997    1
    29998    1
    29999    1
    Name: DEFAULT_NEXT_MONTH, Length: 30000, dtype: int64



############ 23개 feature 중 10개 선택 #############


# define RFE
rfe = RFE(estimator=DecisionTreeClassifier(), n_features_to_select=10)

# fit RFE
rfe.fit(x_data, y_data)

# summarize all features
for i in range(x_data.shape[1]):
  print('Column: %d, Selected=%s, Rank: %d' % (i, rfe.support_[i], rfe.ranking_[i]))
    출력 :
    Column: 0, Selected=True, Rank: 1
    Column: 1, Selected=False, Rank: 12
    Column: 2, Selected=False, Rank: 8
    Column: 3, Selected=False, Rank: 11
    Column: 4, Selected=True, Rank: 1
    Column: 5, Selected=True, Rank: 1
    Column: 6, Selected=False, Rank: 7
    Column: 7, Selected=False, Rank: 9
    Column: 8, Selected=False, Rank: 14
    Column: 9, Selected=False, Rank: 13
    Column: 10, Selected=False, Rank: 10
    Column: 11, Selected=True, Rank: 1
    Column: 12, Selected=True, Rank: 1
    Column: 13, Selected=False, Rank: 5
    Column: 14, Selected=False, Rank: 6
    Column: 15, Selected=True, Rank: 1
    Column: 16, Selected=True, Rank: 1
    Column: 17, Selected=False, Rank: 2
    Column: 18, Selected=True, Rank: 1
    Column: 19, Selected=True, Rank: 1
    Column: 20, Selected=False, Rank: 4
    Column: 21, Selected=False, Rank: 3
    Column: 22, Selected=True, Rank: 1
```



* ###  RFECV

 RFE를 사용할 때에 가장 큰 단점은 몇 개의 feature를 남겨야 할 지를 사용자가 직접 정의해야 한다는 점이다.

 **이러한 단점을 극복하기 위해 등장한 것이 RFECV**이다. RFECV(Recursive Feature Elimination with Cross Validation)는 위의 RFE가 사용하던 방법과 똑같이 가장 feature importance가 낮은 feature들을 제거해가면서 각 feature 개수마다 모델의 성능을 계산한다. 이 때, 각 feature 개수마다 K-fole validation 등의 cross validation을 활용하여 각기 다른 성능을 도출한다. 

이렇게 도출된 **각 feature 개수별 성능을 평균내어 가장 높은 성능을 가지는 feature 개수에 해당하는 feature들을 최종 feature selection 결과로 사용**한다.





---





## 4. 데이터 정규화



 우선 PCA를 수행해주기 전에 **변수들의 단위를 표준화**시켜주어야 한다. 즉, PCA 수행 시 **상관행렬**을 이용해 표준화계수로 만들어준 후 PCA를 수행해야한다.



* #### MinMaxScaler

모든 feature 값이 0~1사이에 있도록 데이터를 재조정한다. 다만 이상치가 있는 경우 변환된 값이 매우 좁은 범위로 압축될 수 있다.

즉, MinMaxScaler 역시 아웃라이어의 존재에 매우 민감하다.

* #### StandardScaler

평균을 제거하고 데이터를 단위 분산으로 조정한다. 그러나 이상치가 있다면 평균과 표준편차에 영향을 미쳐 변환된 데이터의 확산은 매우 달라지게 된다.

따라서 이상치가 있는 경우 균형 잡힌 척도를 보장할 수 없다.





---





## 7. PCA를 통한 차원축소



기존 여러 개의 변수의 차원의 축소를 수행해주면서 추출되는 새로운 변수를 만드는 즉, Feature extraction 중 한 가지 방법 <u>**PCA를 수행할 때 '몇 개'의 변수로 차원을 축소할지 결정하는 기준**</u>



* #### 3-3 실습문제

  ##### credit_cards_dataset.csv 데이터에서 주성분 10개 추출


```python
# example of pca for dimensionality reduction
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
import pandas as pd
from sklearn.preprocessing import StandardScaler

# define dataset
data = pd.read_csv("../Big_Data_Analysis/feature_selection/credit_cards_dataset.csv")
data = data.rename(columns={'default.payment.next.month': 'DEFAULT_NEXT_MONTH'})


# 상관행렬을 이용하기 위한 표준화계수로 만들기 위해 scaling(표준화)
std_df = StandardScaler().fit_transform(data)
std_df = pd.DataFrame(std_df, index=data.index, columns=data.columns)
data = std_df

# id컬럼과 예측값인 y_data를 제거하고 x_data에 data를 할당
x_data = data.drop(['DEFAULT_NEXT_MONTH'],axis=1)
y_data = data['DEFAULT_NEXT_MONTH']
x_data = x_data.drop(['ID'],axis=1)

x_data.info()
    출력 :
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 30000 entries, 0 to 29999
    Data columns (total 23 columns):
     #   Column     Non-Null Count  Dtype  
    ---  ------     --------------  -----  
     0   LIMIT_BAL  30000 non-null  float64
     1   SEX        30000 non-null  float64
     2   EDUCATION  30000 non-null  float64
     3   MARRIAGE   30000 non-null  float64
     4   AGE        30000 non-null  float64
     5   PAY_0      30000 non-null  float64
     6   PAY_2      30000 non-null  float64
     7   PAY_3      30000 non-null  float64
     8   PAY_4      30000 non-null  float64
     9   PAY_5      30000 non-null  float64
     10  PAY_6      30000 non-null  float64
     11  BILL_AMT1  30000 non-null  float64
     12  BILL_AMT2  30000 non-null  float64
     13  BILL_AMT3  30000 non-null  float64
     14  BILL_AMT4  30000 non-null  float64
     15  BILL_AMT5  30000 non-null  float64
     16  BILL_AMT6  30000 non-null  float64
     17  PAY_AMT1   30000 non-null  float64
     18  PAY_AMT2   30000 non-null  float64
     19  PAY_AMT3   30000 non-null  float64
     20  PAY_AMT4   30000 non-null  float64
     21  PAY_AMT5   30000 non-null  float64
     22  PAY_AMT6   30000 non-null  float64
    dtypes: float64(23)
    memory usage: 5.3 MB



# define the transform
trans = PCA(n_components=10)

# transform the data
X_dim = trans.fit_transform(x_data)

# summarize data after the transform
print(X_dim[:5, :])
    출력 :
    [[-1.88796243 -0.90610864 -0.48779485 -0.54001511  0.99795733  0.04440394
      -0.62368663  0.11279392 -0.18989415 -0.0846023 ]
     [-0.76469577 -2.10928757  1.0973135  -0.48347979  0.85898022 -0.23509851
       0.06474189  0.09359503 -0.15369948  0.12403459]
     [-0.8474079  -1.07217896  0.4121783  -0.43356395  0.77049255  0.01866482
      -0.15047282 -0.09188404 -0.15617874  0.08917023]
     [-0.1965886  -0.80902155 -0.81864238  0.29287835  0.90936651 -0.28464438
       0.23522175 -0.06298351  0.11461131 -0.0670063 ]
     [-0.84093409 -0.07253802 -1.00525746  2.32801334 -1.02312356  0.79433054
       0.71106954  0.1241912   0.6025271  -0.30747777]]

```



##### * 참고

##### Make_classification

- Make_classification은 사이킷런의 패키지로 가상의 분류모형 데이터를 생성해주는 함수이다.

##### 매개변수

* n_sample : 표본 데이터의 수 (default=100)
* n_features : 독립변수의 수 (전체 feature의 수) (default=20)
* n_infomative : 독립 변수 중 종속 변수와 상관 관계가 있는 성분의 수 (default = 2)
* n_redundant : 독립 변수 중 다른 독립 변수의 선형 조합으로 나타나는 성분의 수 (default=2)
* n_repeated : 독립 변수 중 단순 중복된 성분의 수 (default=0)
* n_classes : 종속 변수의 클래스 수 (default=2)
* n_clusters_per_class : 클래스 당 클러스터의 수 (default=2)
* weights : 각 클래스에 할당된 표본 수 (default=None)
* flip_y : 클래스가 임의로 교환되는 샘플의 일부, 라벨에 노이즈를 생성하여 분류를 어렵게 만든다(default=0.01)



