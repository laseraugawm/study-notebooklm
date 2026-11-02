# 데이터분석 퀴즈

## Question 1
다음은 딕셔너리와 스택(Stack)을 활용하여 화학식 $C_2H_4$ (에틸렌)의 질량 합을 구하는 파이썬 코드이다. 프로그램 실행 결과로 출력되는 값은?

```python
chemical = 'C2H4'
stack = []
atom = {'H':1, 'C':12, 'O':16}
for c in chemical :
  if c == 'H' or c == 'C' or c == 'O' :
    stack.append(atom[c])
  else :
    stack.append(stack.pop()*int(c))
print(sum(stack))
```

- [x] 28
- [ ] 26
- [ ] 16
- [ ] 13

**Hint:** C2H4에서 탄소 원자 2개(12 × 2)와 수소 원자 4개(1 × 4)의 질량을 각각 연산한 후 스택의 총합을 구해 보세요.

## Question 2
탐색적 데이터 분석을 활용한 문제 해결 과정 중 '협력 활동'으로 진행되는 단계만을 올바르게 짝지은 것은?

- [x] 단계 1 (문제 정의하기), 단계 4 (문제 해결하기)
- [ ] 단계 2 (데이터 수집하기), 단계 3 (데이터 분석하기)
- [ ] 단계 1 (문제 정의하기), 단계 2 (데이터 수집하기)
- [ ] 단계 3 (데이터 분석하기), 단계 4 (문제 해결하기)

**Hint:** 주제 설정 및 해결 방안을 토의하는 첫 단계와 마지막 단계가 모둠원 간의 협력이 요구되는 활동입니다.

## Question 3
유엔(UN)의 1인당 음식물 쓰레기 데이터셋에서 'Food Waste Sector' 컬럼의 항목 코드와 그 설명이 바르게 연결된 것은?

- [x] HHS — 가정 (HouseHold)
- [ ] OOHC — 소매업 (Retail)
- [ ] RTL — 외식 산업 (Out-Of-Home Catering)
- [ ] ALL — 가공업 (Manufacturing)

**Hint:** 'HouseHold'의 영문 약자가 어느 분야를 나타내는지 확인해 보세요.

## Question 4
파이썬 판다스(Pandas) 라이브러리를 사용해 데이터프레임 `df`를 처리하는 코드 설명 중 올바르지 않은 것은?

- [x] `df.info()`는 데이터프레임 상위 5개 행의 데이터를 미리보기로 출력하는 함수이다.
- [ ] `df.rename(columns = {'2019':'PC2019'})`는 '2019' 컬럼명을 'PC2019'로 변경한다.
- [ ] `df1 = df[df['Food Waste Sector'] == 'ALL']` 조건을 만족하는 행들만 필터링하여 새로운 데이터프레임 `df1`을 만든다.
- [ ] 추출된 조건 결과를 `df1`과 같은 별도 변수에 저장하면 추후 동일 조건의 재작성 없이 데이터를 재사용할 수 있다.

**Hint:** 데이터프레임의 상위 5개 행 데이터를 출력할 때 사용하는 메서드는 `df.head()`입니다.

## Question 5
판다스 데이터프레임 정렬 및 조건 추출 코드에 대한 설명으로 옳은 것은?

```python
df1 = df1.sort_values("PC2019", ascending = False)
df2 = df[df["Food Waste Sector"].isin(["HHS", "OOHC", "RTL"])]
```

- [x] `ascending = False` 옵션은 지정된 컬럼을 기준으로 데이터를 내림차순 정렬한다.
- [ ] `sort_values` 함수는 데이터프레임의 행 인덱스 번호를 정렬하는 함수이다.
- [ ] `isin` 함수는 인자로 전달된 리스트 값들을 제외한 나머지 행들만 선택한다.
- [ ] `ascending = True`로 설정하면 가장 값이 큰 데이터부터 상위에 배치된다.

**Hint:** 내림차순(Descending) 정렬 옵션의 불리언(Boolean) 값 설정을 확인하세요.

## Question 6
다음 파이썬 Matplotlib 시각화 코드에서 사용된 `autopct = "%.1f%%"` 옵션의 역할로 올바른 것은?

```python
import matplotlib.pyplot as plt
label = ["HHS", "OOHC", "RTL"]
plt.pie(korea["PC2019"], labels = label, autopct = "%.1f%%"
plt.show()
```

- [x] 원형 그래프 각 항목의 비율을 계산하여 소수점 첫째 자리까지 퍼센트(%)로 표시한다.
- [ ] 원형 그래프의 전체 반지름 크기를 1.0 단위로 자동 설정한다.
- [ ] 그래프의 범례(legend) 이름을 외부 리스트 데이터로 지정한다.
- [ ] 원형 그래프 항목 간의 투명도를 0.1 단위로 지정하는 옵션이다.

**Hint:** `autopct`에서 'pct'는 percentage의 약자이고 `%.1f`는 소수점 첫째 자리 실수를 의미합니다.

## Question 7
유엔 데이터 분석 결과, 대한민국 1인당 음식물 쓰레기 현황에 관한 설명으로 가장 적절한 것은?

- [x] 대한민국의 1인당 음식물 쓰레기 비중이 가장 높게 나타나는 곳은 일반 가정(HHS)이다.
- [ ] 대한민국은 외식 산업(OOHC)에서 발생하는 음식물 쓰레기 비율이 50% 이상을 넘는다.
- [ ] 대한민국은 소매업(RTL)의 1인당 음식물 쓰레기 배출 비중이 가정(HHS)보다 크다.
- [ ] 대한민국의 1인당 음식물 쓰레기 총량은 전 세계에서 가장 적은 축에 속한다.

**Hint:** 가정(HHS, 65%), 외식 산업(OOHC, 23.3%), 소매업(RTL, 11.7%)의 비중을 서로 비교해 보세요.

## Question 8
다음 파이썬 코드의 실행 결과로 올바른 것은?

```python
prefix = "Super"
repeat_str = "sub-"
suffix = "structure"
print(prefix + repeat_str * 2 + suffix)
```

- [x] Supersub-sub-structure
- [ ] Super sub- sub- structure
- [ ] Supersub-structure2
- [ ] Super2sub-structure

**Hint:** 파이썬에서 문자열에 정수 $n$을 곱하면 문자열이 $n$번 반복하여 연결됩니다.

## Question 9
다음 파이썬 코드의 실행 결과로 출력되는 문자열은?

```python
pattern = ['A', 'B', 'C', 'D']
indices = [3, 0, 2, 0, 1]
result = ""
for idx in indices :
    result += pattern[idx]
print(result)
```

- [x] DACAB
- [ ] DCABA
- [ ] ABCDA
- [ ] BACAD

**Hint:** 파이썬의 리스트 인덱스는 0부터 시작하므로 pattern[0]='A', pattern[1]='B', pattern[2]='C', pattern[3]='D'입니다.

## Question 10
다음 설명에 해당하는 데이터 모델링 방법으로 가장 적절한 것은?

> "나무의 뿌리에서 가지가 뻗어 나가는 형태와 비슷하며, 데이터 간의 계층적인 관계를 표현하기에 매우 적합한 데이터 구조이다."

- [x] 트리 (Tree)
- [ ] 그래프 (Graph)
- [ ] 표 (Table)
- [ ] 히트맵 (Heatmap)

**Hint:** 나무(Tree)의 뿌리와 가지 구조에서 이름을 딴 알고리즘/자료구조 명칭을 떠올려 보세요.
