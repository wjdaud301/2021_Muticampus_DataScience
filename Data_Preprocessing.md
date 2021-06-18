## Data Preprocessing 데이터 전처리

#### - Data Preprocessing 핵심 전략



Data의 기본적인 정보들을 수집

- 결측값은 어떻게 처리하지? 값은 어떻게 바꿔주지?
- 데이터 형태는 어떻게 되어있지(범주형, 연속형)? 어떻게 처리하지?
- 데이터의 scale은 어떻게 맞춰주지?



### 1. 결측치 missing value 처리

결측치 처리 전략

- 데이터가 NaN일 때 그대로 날려버린다(complete drop)
- 데이터가 없는 최소의 개수와 같이 규칙을 정해서 날려버린다
- 데이터가 거의 없는 feature는 feature 자체를 날려버린다
- 최빈값, 평균값으로 NaN을 채워버린다
- <u>**SMOTE, KNN 같은 방법을 사용해서 근사한 instance의 값으로 채우기(가장 과학적인 방법)**</u>



#### Missing value 처리하기

(1) 결측치 확인하기

```python
# nan값이 얼마나 있는지 column별로 확인하기
df.isnull().sum()

# 전체 data 개수 대비 Nan의 비율
df.isnull().sum() / len(df)
```



(2) 결측지 row 날려버리기

```python
# 튜플에서 데이터가 하나라도 없으면 날려버리기
df = df.dropna()

# 모든 데이터가 NaN일 때만 날려버리기
df = df.dropna(how='all')

# column을 기준으로 nan 값이 4개 이상이면 해당 column 날려버리기
df = df.dropna(axis=1, thres=3)
```



(3) 결측지를 채워버리기

```python
# NaN을 0으로 채워버리기
df.fillna(0)

# 평균값으로 채워버리기
df['col1'].fillna(df['col1'].mean(), inplace=True)

# 그룹 범주로 나눠서 그룹별 평균값으로 채워버리기
df['col1'].fillna(df.groupby('sex')['col1'].transform('mean'), inplace=True)
df[df['A'].notnull() & df['B'].notnull()] # 컬럼 A와 B 모두 Null이 아닌 경우만 표시
```



---



### 2. 범주형 변수 categorical data 처리



일반적으로 범주형 데이터를 분석하기 위해서 더미(dummy) 변수화합니다.

다른 말로는 원핫인코딩(one-hot encoding)이라고 합니다.



#### 범주형 변수 처리 전략

- One Hot Encoding
- Data Binding

Pandas를 사용해서도 쉽게 범주형 변수를 처리할 수 있으며,

Scikit-learn의 preprocessing 패키지에서 **labeling**과 **one-hot encoding** 기능을 사용하는 것이 deployment를 고려했을 때 권장하는 되는 방법입니다.



### Categorical variable 처리하기

#### (1) One Hot Encoding

```python
# 데이터프레임에서 object 타입으로 되어있는 변수는 dummy 변수화
pd.get_dummies(df)


# 특정 컬럼에 대해서만 dummy 변수화한 df 반환
pd.get_dummies(df['colA'])
pd.get_dummies(df[['colA']]) #대괄호가 두번 들어가면 prefix로 변수명이 붙어서 반환


# Numeric으로 되어있지만 실제로는 범주형인 데이터인 경우 object type으로 변환하면서 dummy 변수화
sex_dict = {1:'M', 2:'F', 3:'E'}
df['sex'] = df['sex'].map(sex_dict)

sex = pd.get_dummies(df['sex'])
pd.concat([df, sex, axis=1)
del df['sex']
```



Scikit-learn의 preprocessing object를 사용하는 이유는 이후에 deployment 단계에서 object 형태로 새로운 데이터에도 동일한 적용을 할 수 있어야 하기 때문에 사용합니다.

pickle 등으로 object를 저장해서 필요할 때 불러와서 사용할 수도 있습니다.



```python
rom sklarn import preprocessing

le = preprocessing.LabelEncoder()  #dict를 통해서 labeling하는 것과 동일한 결과를 제공
le.fit(data[:,0]) # 첫번째 컬럼을 기준으로 label 규칙을 저장
le.transform(data[:,0])

# label column 별로 Label Encoder object 생성하기
label_column = [0,1,2,5] # Series 형태로 넣어줘야하므로 iloc 방식으로 특정 컬럼만 지정
label_encoder_list = []
for column_index in label_column:
    le = preprocessing.LabelEncoder()
    le.fit(data[:, column_index])
    label_encoder_list.append(le) #각 컬럼 별로 label encoder 저장
    del le

# 생성한 encoder로 해당 컬럼 labeling 적용하기
label_encoder_list[0].transform(data[:,0])


# one hot encoding
ohe = preprocessing.OneHotEncoder()  # data가 숫자형식으로 들어가야하므로 위의 LabelEncoder가 필요
ohe.fit(data[:,0].reshape(-1,1))  # reshape을 통해서 2-dimension 형태로 변환해야 한다.
ohe.transform(data[:,0].reshape(-1, 1))

# labeling된 column 별로 One Hot Encoder object 생성하기
ohe_column = [0,1,2,5] # column index와 label encoder index
onehot_encoder_list = []
for column_index in ohe_column:
    ohe = preprocessing.OneHotEncoder()
    ohe.fit(data[:, column_index])
    onehot_encoder_list.append(ohe) #각 컬럼 별로 label encoder 저장
    del ohe

```



#### (1) Data Binning

연속형 데이터를 구간으로 나누어 범주화하는 방법

```python
bins = [0, 25, 50, 75, 100] # 구간을 설정한다. (0~25, ... , 75~100)
bins_names = ['A', 'B', 'C', 'D', 'E'] # 구간별 이름
categories = pd.cut(df['score'], bins, labels=bins_names)
categories
```



---



## 3. Feature Scaling

신경망 모델 뿐만 아니라 Ridge, Lasso 같은 선형회귀 모델에서도 데이터의 feature를 맞춰줘야 할 필요가 있습니다.

데이터의 값이 너무 크거나 작아 변수의 영향이 제대로 반영되지 않으며,

알고리즘의 계산 과정에서 0으로 수렴하거나 값이 너무 커져버리거나 할 수 있습니다.

feature scaling은 아주 중요합니다.



#### Feature scaling 전략

- Min-Max Normalization
- Standardization



### Feature Scaling

#### (1) Min-Max Nomarlization

```python
from sklearn.preprocessing import minmax_scale, StandardScaler, MinMaxScaler
df['A'].apply(minmax_scale)


# object로 만들어 재사용하기 위한 방법 (위의 one-hot encoding 방법과 동일)
minmax_scale = MinMaxScaler(feature_range=[0,1]).fit(df[['A', 'B']]) # A, B 컬럼 각각 standard_scaler가 만들어짐
df_minmax = minmax_scale.transform(df[['A', 'B']])
```



#### (2) Standardization

```python
# object로 만들어 재사용하기 위한 방법 (위의 one-hot encoding 방법과 동일)
df['A'].apply(lambda x: StandardScaler(x))
std_scale = StandardScaler().fit(df[['A', 'B']]) # A, B 컬럼 각각 standard_scaler가 만들어짐
df_std = std_scale.transform(df[['A', 'B']])
```









출처: https://sacko.tistory.com/60 [데이터 분석하는 문과생, 싸코]






