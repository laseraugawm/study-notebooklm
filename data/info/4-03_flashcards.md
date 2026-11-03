# 기계학습 플래시카드

## Card 1

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '단순 선형 회귀와 다중 선형 회귀의 주요 차이점은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '단순 선형 회귀는 하나의 특징에 따른 결과를 예측하고, 다중 선형 회귀는 두 개 이상의 특징에 따른 결과를 예측한다.'}]}

---

## Card 2

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "기계학습 모델 구축 시 '훈련 데이터'와 '테스트 데이터'의 역할 차이는 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '훈련 데이터는 모델의 학습에 사용되는 데이터이며, 테스트 데이터는 학습을 마친 모델의 예측 성능을 평가하는 데 사용되는 데이터이다.'}]}

---

## Card 3

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '지도학습의 분류 문제에서 특정 입력 데이터가 속하는 범주(클래스) 값을 무엇이라고 부르는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '레이블(Label)'}]}

---

## Card 4

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '회귀 모델과 분류 모델이 출력하는 예측 결과의 형태 차이는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '회귀 모델은 성적 점수나 기온과 같은 연속적인 수치형 데이터를 예측하고, 분류 모델은 합격/불합격이나 펭귄 종과 같은 범주형 데이터를 예측한다.'}]}

---

## Card 5

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '트리 구조를 기반으로 각 분기마다 특징에 대한 분류 기준을 만들어 데이터를 분류하는 알고리즘은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '결정트리(Decision Tree)'}]}

---

## Card 6

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '결정트리 알고리즘에서 트리의 깊이가 지나치게 깊어질 때 발생하는 문제점은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '분류 기준이 너무 많아져 새로운 데이터에 대한 예측 성능이 오히려 떨어질 수 있다.'}]}

---

## Card 7

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '결정트리 알고리즘은 분류 문제와 회귀 문제 중 어느 분야에 적용 가능한가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '분류 문제와 회귀 문제 모두에 적용할 수 있다.'}]}

---

## Card 8

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "명칭에 '회귀'가 들어가지만 실제로는 데이터를 $0$과 $1$ 사이의 확률값으로 예측하여 클래스를 구별하는 대표적인 선형 분류 모델은 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '로지스틱 회귀(Logistic Regression)'}]}

---

## Card 9

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '로지스틱 회귀 모델에서 예측된 확률값을 바탕으로 이진 분류를 수행할 때 주로 사용되는 기준값은 얼마인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '$0.5$ (확률이 $0.5$ 이상이면 가능성이 더 높은 클래스로 분류)'}]}

---

## Card 10

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '새로운 데이터가 입력되었을 때 가장 가까운 $k$개의 이웃 데이터 클래스를 확인하고 다수결로 분류하는 알고리즘은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'k-최근접 이웃(kNN, k-Nearest Neighbor) 알고리즘'}]}

---

## Card 11

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '두 점 $P_1(1,1)$과 $P_2(5,4)$ 사이의 유클리디안 거리와 맨하튼 거리는 각각 얼마인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '유클리디안 거리는 $5$이며, 맨하튼 거리는 $7$이다. (유클리디안: $\\sqrt{(5-1)^2 + (4-1)^2} = 5$, 맨하튼: $|5-1| + |4-1| = 7$)'}]}

---

## Card 12

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': 'kNN이나 로지스틱 회귀와 같은 거리 기반 알고리즘을 사용하기 전에 데이터 속성 간 스케일을 맞추기 위해 수행해야 하는 전처리 작업은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '데이터 정규화(Normalization)'}]}

---

## Card 13

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '사람의 뇌 신경계에서 수많은 뉴런이 신호를 주고받는 방식을 모방한 기계학습 모델은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '인공 신경망(ANN)'}]}

---

## Card 14

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '인공 신경망의 연결이 깊어져 더욱 복잡한 문제를 해결할 수 있도록 발전한 모델을 무엇이라고 하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '심층 신경망(DNN)'}]}

---

## Card 15

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '정답(레이블)이 없는 데이터의 특징을 분석하여 유사한 특성을 가진 데이터끼리 그룹화하는 비지도학습 기법은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '군집화(Clustering)'}]}

---

## Card 16

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '군집화(Clustering)를 수행할 때 바람직한 군집 분할의 조건은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '같은 군집에 속하는 데이터 간 유사성은 높고, 서로 다른 군집에 속하는 데이터 간 차이는 크게 나도록 분할하는 것이다.'}]}

---

## Card 17

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "지도학습의 '분류'와 비지도학습의 '군집화'의 주된 목적 차이는 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '분류는 입력 데이터의 범주(종류)를 판별하는 것이 목적이고, 군집화는 형성된 그룹의 정보를 해석하고 활용하는 것이 목적이다.'}]}

---

## Card 18

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '주어진 데이터를 $K$개의 군집으로 묶고, 각 군집의 중심점 위치를 속한 데이터들의 평균으로 갱신해 나가는 비지도학습 알고리즘은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'K-평균(K-means) 군집화 알고리즘'}]}

---

## Card 19

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': 'K-평균 군집화 알고리즘에서 군집화의 성능이 좋다고 판단하는 거리의 조건은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '군집 안의 데이터와 해당 군집 중심점 사이의 거리가 가까울수록 우수하다.'}]}

---

## Card 20

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "거래 데이터 등에서 구매 항목 사이의 관련성을 분석하여 '우유를 구매하면 식빵도 구매한다'와 같은 규칙을 발견하는 기술은 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '연관 규칙(Association Rules)'}]}

---

## Card 21

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '기계학습을 이용한 문제 해결 과정 4단계를 순서대로 나열하시오.'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '[문제 정의하기] $\\rightarrow$ [데이터 수집 및 전처리하기] $\\rightarrow$ [모델 선정 및 학습하기] $\\rightarrow$ [모델 평가하기]'}]}

---

## Card 22

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "기계학습 구현 과정 중 '단계1 문제 정의하기'에서 수행하는 주된 활동은 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '해결할 문제를 발견하고 명확히 한 후, 기계학습으로 해결할 수 있는 문제인지 판단한다.'}]}

---

## Card 23

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "기계학습 구현 과정 중 '단계2 데이터 수집 및 전처리하기'에서 전처리를 수행하는 핵심 이유는 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '데이터의 결측치나 이상치를 처리하여 기계학습 모델 학습에 적합한 형태로 가공하기 위해서이다.'}]}

---

## Card 24

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '체질량 지수(BMI) 구하기와 같이 명확한 수학적 수식이나 단순 규칙이 존재하는 문제를 해결할 때 효율적인 접근 방식은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '전통적인 프로그래밍 방법'}]}

---

## Card 25

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '의료 영상에서 질환 진단하기나 이미지로 개/고양이를 구분하는 것처럼 규칙과 알고리즘을 사람이 명확히 작성하기 어려운 문제를 해결하는 방식은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '대량의 데이터로부터 스스로 규칙을 찾는 기계학습 방식'}]}

---

## Card 26

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '텍스트 코딩 없이 캔버스에 위젯을 드래그 앤 드롭하여 기계학습 및 데이터 분석을 수행할 수 있는 오픈소스 소프트웨어는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3(Orange3)'}]}

---

## Card 27

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3의 File 위젯 설정에서 예측의 기준이 되는 입력 데이터 컬럼의 Role을 무엇으로 지정하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'feature'}]}

---

## Card 28

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3의 File 위젯에서 모델이 최종 예측해야 하는 레이블 컬럼의 Role을 무엇으로 지정하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'target'}]}

---

## Card 29

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3에서 학습에 필요 없어서 제외하려는 컬럼의 Role은 무엇으로 지정해야 하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'skip'}]}

---

## Card 30

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '회귀 모델 평가 지표인 MSE, RMSE, MAE는 수치가 어떠할수록 예측 모델이 우수하다고 평가하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '수치가 작을수록 실젯값과 예측값의 오차가 적어 우수한 모델이다.'}]}

---

## Card 31

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '회귀 모델의 적합도를 나타내는 $R^2$(결정계수) 지표는 수치가 얼마에 가까울수록 성능이 좋은가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '$1$에 가까울수록 성능이 우수하다.'}]}

---

## Card 32

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3에서 전체 데이터를 훈련 데이터(예: 70%)와 테스트 데이터(예: 30%)로 분할할 때 사용하는 위젯은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'Data Sampler 위젯'}]}

---

## Card 33

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '분류 모델의 대표적인 성능 평가 지표인 CA(Classification Accuracy)의 의미는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '분류 정확도를 뜻하며, 모델이 입력된 데이터를 얼마나 정확히 정답 클래스로 분류하는지 비율로 나타낸 값이다.'}]}

---

## Card 34

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '오렌지3에서 결정트리로 학습된 분류 모델의 트리 구조와 기준 속성을 시각적으로 파악할 때 사용하는 위젯은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'Tree Viewer 위젯'}]}

---

## Card 35

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '결정트리의 Tree Viewer 시각화 결과에서 최상단 루트 노드에 놓인 특징이 의미하는 바는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '해당 데이터를 구분하고 분류하는 데 가장 결정적이고 영향력이 큰 특징임을 의미한다.'}]}

---

## Card 36

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '구글에서 제공하는 웹 기반 플랫폼으로, 블록 코딩이나 설치 없이 이미지를 촬영/업로드하여 분류 모델을 빠르게 만드는 도구는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '티처블머신(Teachable Machine)'}]}

---

## Card 37

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '티처블머신과 같은 이미지 학습 도구에서 학습 성능을 높이기 위한 좋은 이미지 데이터의 조건 2가지는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '배경이 단순한 이미지, 사물이 확대되어 형태가 뚜렷하게 잘 보이는 이미지.'}]}

---

## Card 38

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '기계학습 모델이 특정 입력 데이터에 대해 해당 클래스일 확률(확신도)을 나타내는 지표를 무엇이라고 부르는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': 'Confidence Score (신뢰 점수)'}]}

---

## Card 39

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '웹 브라우저 상에서 인터랙티브하게 파이썬 코드를 작성하고 실행할 수 있는 오픈소스 개발 환경은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '주피터 노트북(Jupyter Notebook)'}]}

---

## Card 40

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': 'OpenCV 라이브러리를 이용하여 컴퓨터의 기본 웹 카메라를 연결하는 파이썬 명령문은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '`cv2.VideoCapture(0)`'}]}

---

## Card 41

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '이미지 처리 모델 입력 단계에서 `(image / 127.5) - 1` 연산을 수행하는 주된 목적은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '$0$~$255$ 범위의 픽셀 값을 $-1$에서 $1$ 사이의 값으로 변환하는 이미지 배열 정규화(Normalization)이다.'}]}

---

## Card 42

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '주변 환경과 지속적으로 상호 작용하면서 자율적으로 지능적인 판단과 결정을 내려 행동하는 시스템을 무엇이라고 하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '지능 에이전트(Intelligent Agent)'}]}

---

## Card 43

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '지능 에이전트를 분석하는 4가지 주요 요소는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '환경, 인식, 학습과 추론, 행동'}]}

---

## Card 44

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "스팸 메일 분류 지능 에이전트에서 '메일함의 다양한 메일'은 4가지 구성 요소 중 어디에 속하는가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '환경'}]}

---

## Card 45

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "스팸 메일 분류 에이전트가 탐지된 스팸 메일을 '스팸 메일함으로 이동'시키는 것은 4가지 요소 중 어디에 해당하는가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '행동'}]}

---

## Card 46

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '신용카드 사용 패턴이나 쇼핑 사이트의 구매 이력을 기반으로 비슷한 성향의 고객을 세분화하는 기계학습 기법은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '비지도학습의 군집화(Clustering)'}]}

---

## Card 47

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '방의 면적 및 건물 연식 데이터와 실제 주택 가격 데이터를 함께 학습시켜 새로운 집값을 예측하는 모델은 지도학습 중 어디에 해당하는가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '회귀(Regression)'}]}

---

## Card 48

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': "비지도학습 방식인 군집화의 결과에 대해 정답이 '맞다' 또는 '틀렸다'라고 단정할 수 없는 이유는 무엇인가?"}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '군집화는 정답(레이블)이 부여되지 않은 상태에서 특징의 유사성만으로 묶은 것이므로 결과 정보를 해석하고 활용하는 것이 목적이기 때문이다.'}]}

---

## Card 49

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '결정트리 모델이 $2$차원 속성 공간에서 클래스를 구분하기 위해 경계를 형성할 때 나타나는 기하학적 특징은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '$x$축과 $y$축에 수평 또는 수직한 직선 형태의 분류 경계를 그으며 공간을 분할한다.'}]}

---

## Card 50

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': 'k-최근접 이웃(kNN) 알고리즘에서 $k$의 값을 $1$에서 $5$로 변경할 때 발생할 수 있는 주요 변화는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '참고하는 다수결 이웃의 범위가 늘어나므로 동일한 데이터에 대한 분류 예측 클래스가 변경될 수 있다.'}]}

---

## Card 51

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': 'K-평균 군집화 알고리즘을 사용하기 전에 사용자가 직접 사전에 설정해 주어야 하는 매개변수는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '묶고자 하는 군집의 개수($K$)'}]}

---

## Card 52

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '지폐의 위/아래 여백 수치 데이터로부터 위조지폐 여부를 판단하기 위해 직선 경계선을 형성하는 대표적인 선형 분류 모델은 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '로지스틱 회귀(Logistic Regression)'}]}

---

## Card 53

**Q:** {'flashcardContentBlock': [{'type': 'text', 'content': '군집화 알고리즘에서 데이터 개체들 간의 유사성을 판별할 때 측정 기준으로 사용되는 핵심 수치는 무엇인가?'}]}

**A:** {'flashcardContentBlock': [{'type': 'text', 'content': '데이터 간의 거리 (유클리디안 거리 또는 맨하튼 거리)'}]}

---
