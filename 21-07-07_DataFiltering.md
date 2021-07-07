## [Python] :: Pandas 특정 조건을 만족하는 Data Filtering

* #### 샘플 데이터 불러오기

```python
# 판다스 라이브러리 임포트
import pandas as pd
# plotly express에 내장되어있는 gapminder 데이터프레임을 사용하겠습니다.
import plotly.express as px
# plotly가 설치되어있지 않다면 아래 명령으로 설치할 수 있습니다.
# !pip install plotly
```

```python
df = px.data.gapminder()
```





* #### 특정 조건을 만족하는 데이터 필터링하기

특정 조건을 만족하는 행을 필터링하는 방법은 크게 세 가지 단계를 거칩니다.

1. 컬럼을 선택합니다.

2. 컬럼의 데이터와 특정 조건을 비교합니다. 조건을 만족하는 경우에는 True, 아닌 경우에는 False 반환합니다.

3. 비교 결과를 이용해서 데이터프레임에서 일부 데이터를 추출합니다.





* #### 특정 값과 일치하는 데이터 필터링하기

country 컬럼의 값이 Venezuela인 데이터를 필터링하기

```python
# country 컬럼을 선택합니다.
# 컬럼의 값과 조건을 비교합니다.
is_venezuela = df['country'] == 'Venezuela'

# 조건를 충족하는 데이터를 필터링하여 새로운 변수에 저장합니다.
venezuela = df[is_venezuela]

# 결과를 출력합니다.
venezuela
```





* #### **두가지 조건을 만족하는 데이터 필터링하기**

**1) continent 컬럼의 값이 Asia**이면서 **2) lifeExp 컬럼의 값이 80 이상**인 데이터를 필터링하기

```python
# continent 컬럼을 선택합니다.
# 컬럼의 값과 조건을 비교합니다.
is_asia = df['continent'] == 'Asia'

# lifeExp 컬럼을 선택합니다.
# 컬럼의 값과 조건을 비교합니다.
lifeExp_greather_80 = df['lifeExp'] >= 80

# 두가지 조건를 동시에 충족하는 데이터를 필터링하여 새로운 변수에 저장합니다. (AND)
subset_df = df[is_asia & lifeExp_greather_80]

# 결과를 출력합니다.
subset_df

# 같은 방법
subset_df = df[(df['continent'] == 'Asia') & (df['lifeExp'] >= 80)]
```





* #### 제외 조건을 만족하는 데이터 필터링하기

country 컬럼의 값이 Japan이 아닌 데이터를 필터링하기

```python
# continent 컬럼을 선택합니다.
# 컬럼의 값과 조건을 비교합니다.
not_japan = df['country'] != 'Japan'

# 조건를 충족하는 데이터를 필터링하여 새로운 변수에 저장합니다.
subset_df = df[not_japan]

# 결과를 출력합니다.
print(subset_df.shape)
print()

subset_df.head()
```

== **같은방식**

```python
# continent 컬럼을 선택합니다.
# 컬럼의 값과 조건을 비교합니다.
is_japan = df['country'] == 'Japan'

# 조건를 충족하지 않는 데이터를 필터링하여 새로운 변수에 저장합니다.
subset_df = df[~is_japan]

# 결과를 출력합니다.
print(subset_df.shape)
print()

subset_df.head()
```



* #### **특정 문자열을 포함하는 데이터 필터링하기**

특정 단어가 포함된 데이터를 필터링하기 위해서는 [.str.contains()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html)라는 함수를 사용해야합니다.
이 함수는 해당 컬럼의 값에 특정 문자열이 포함(contains)되어 있을 경우에는 True, 아닌 경우에는 False를 반환합니다.



```python
# country 컬럼을 선택합니다.
# 컬럼의 값에 Korea 또는(|) Japan이라는 문자열이 포함되어있는지 판단합니다.
# 그 결과를 새로운 변수에 할당합니다.
contains_korea_or_japan = df['country'].str.contains("Japan|Korea")

# 조건를 충족하는 데이터를 필터링하여 새로운 변수에 저장합니다.
subset_df = df[contains_korea_or_japan]

# 결과를 출력합니다.
print(subset_df.shape)
print()

subset_df
```



* #### 데이터를 필터링하는 다른방법

```python
# df.query(조건식)
gapminder_asia = gapminder.query("continent == 'Asia'")
```

