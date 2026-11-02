# 파이썬 퀴즈

## Question 1
객체지향 프로그래밍의 기본 개념인 객체, 클래스, 인스턴스에 대한 설명으로 옳은 것은?

- [ ] 인스턴스는 객체를 만들기 위한 설계도로, 공통된 속성과 메소드를 정의한 것이다.
- [ ] 클래스가 가진 특성을 메소드라고 하며, 클래스가 가진 기능을 속성이라고 한다.
- [x] 인스턴스는 클래스와 객체의 관계를 중심으로 설명할 때 주로 사용되며, 어떤 클래스의 구체적인 실체를 의미한다.
- [ ] 하나의 클래스를 정의하면 생성할 수 있는 인스턴스의 개수는 오직 1개로 제한된다.

**Hint:** 설계도에 해당하는 개념과 구체적인 실체에 해당하는 개념을 구분해 보세요.

## Question 2
파이썬 PIL 라이브러리를 사용하여 이미지를 처리할 때, `img.rotate(50)` 명령어가 수행하는 동작으로 옳은 것은?

- [ ] 이미지를 시계 방향(오른쪽)으로 50도 회전시킨다.
- [x] 이미지를 반시계 방향(왼쪽)으로 50도 회전시킨다.
- [ ] 이미지를 좌우로 반전시킨다.
- [ ] 이미지의 상하 위치를 뒤집는다.

**Hint:** 양수 매개변수가 회전시킬 방향(시계방향 또는 반시계방향)을 떠올려 보세요.

## Question 3
PIL 라이브러리의 ImageFilter 모듈에서 지원하는 속성과 그 효과에 대한 설명으로 옳은 것은?

- [ ] CONTOUR 속성은 주변 픽셀의 가중치를 음수로 하여 이미지를 선명하게 만든다.
- [ ] SHARPEN 속성은 이미지 경계를 추출하여 테두리를 그리고 나머지는 흰색으로 처리한다.
- [x] BLUR 속성은 픽셀과 주변 픽셀들의 평균값을 구해 이미지를 뿌옇게 표현한다.
- [ ] BLUR 속성은 픽셀 간의 차이를 극대화하여 이미지의 테두리만 강조한다.

**Hint:** 픽셀과 주변 픽셀들의 평균값을 계산하여 이미지를 처리할 때 나타나는 효과를 생각해 보세요.

## Question 4
PIL 라이브러리에서 이미지를 좌우로 반전시키고자 할 때 사용하는 올바른 코드 표현은?

- [x] img.transpose(Image.FLIP_LEFT_RIGHT)
- [ ] img.transpose(Image.FLIP_TOP_BOTTOM)
- [ ] img.rotate(Image.FLIP_LEFT_RIGHT)
- [ ] img.filter(Image.FLIP_LEFT_RIGHT)

**Hint:** 이미지 반전 메소드 `transpose`에 전달되는 상수를 확인하세요.

## Question 5
파이썬에서 클래스를 정의하고 생성자를 작성할 때의 규칙으로 옳은 것은?

- [x] 생성자는 def __init__(self): 형태로 작성하며 인스턴스 생성 시 속성값을 초기화한다.
- [ ] 메소드를 정의할 때 첫 매개변수인 self는 생략하는 것이 일반적이다.
- [ ] self 키워드는 클래스 자체를 의미하며 특정 인스턴스와는 관련이 없다.
- [ ] 생성자 작성 시 외부에서 속성값을 전달받기 위한 매개변수를 추가할 수 없다.

**Hint:** 생성자의 역할과 메소드 정의 시 첫 번째 매개변수로 들어가는 키워드를 생각해 보세요.

## Question 6
다음은 주사위를 객체지향 방식으로 표현한 파이썬 코드이다. 코드 설명으로 옳지 않은 것은?

```python
import random

class Dice :
    def __init__(self) :
        self.value = 0
    def roll(self) :
        self.value = random.randint(1, 6)
    def get_value(self) :
        return self.value
```

- [ ] dice1 = Dice() 문장을 실행하면 value 속성이 0으로 초기화된 인스턴스가 만들어진다.
- [ ] roll() 메소드는 1부터 6까지의 임의의 정수를 추출하여 value 속성에 저장한다.
- [x] dice1 인스턴스에서 주사위 값을 반환받으려면 Dice.get_value() 형식으로 호출한다.
- [ ] dice1과 dice2 두 개의 인스턴스를 만들어 각각 독립적인 주사위 값을 가질 수 있다.

**Hint:** 생성된 인스턴스를 통해 메소드를 호출할 때의 올바른 문법 형태를 확인해 보세요.

## Question 7
두 이미지 파일의 픽셀을 비교하여 다른 픽셀을 빨간색으로 변경하는 클래스의 일부분이다. (가)와 (나) 빈칸에 들어갈 PIL 라이브러리의 메소드로 알맞게 짝지어진 것은?

```python
def compare(self) :
    for x in range(self.img1.width) :
        for y in range(self.img1.height) :
            if self.img1.____(가)____((x, y)) != self.img2.____(가)____((x, y)) :
                self.new_img.____(나)____((x, y), (255, 0, 0))
    return self.new_img
```

- [x] (가) getpixel, (나) putpixel
- [ ] (가) putpixel, (나) getpixel
- [ ] (가) readpixel, (나) writepixel
- [ ] (가) getcolor, (나) setcolor

**Hint:** 특정 좌표의 픽셀 값을 가져오는 메소드와 픽셀 값을 설정하는 메소드의 이름을 구분해 보세요.

## Question 8
다음과 같은 상보적 전사 규칙(T->A, A->U, C->G, G->C)을 적용하여, DNA 염기 서열 "ATGCGGCGG"를 RNA 서열로 전사했을 때 얻을 수 있는 결과로 옳은 것은?

- [x] "UACGCCGCC"
- [ ] "TACGCCGCC"
- [ ] "ATGCGGCGG"
- [ ] "UACGCGGCC"

**Hint:** DNA의 각 염기가 상보적인 RNA 염기(A, U, C, G)로 어떻게 바뀌는지 일대일로 대입해 보세요.

## Question 9
DNA 서열을 RNA 서열로 전사하는 다음 파이썬 조건문 구조에서, 입력된 염기가 'C'일 때 수행되는 동작으로 옳은 것은?

```python
for i in DNA :
    if i == 'T' :
        RNA = RNA + 'A'
    elif i == 'A' :
        RNA = RNA + 'U'
    elif i == 'C' :
        RNA = RNA + 'G'
    else :
        RNA = RNA + 'C'
```

- [ ] RNA 변수 뒤에 'A'를 이어 붙인다.
- [ ] RNA 변수 뒤에 'U'를 이어 붙인다.
- [x] RNA 변수 뒤에 'G'를 이어 붙인다.
- [ ] RNA 변수 뒤에 'C'를 이어 붙인다.

**Hint:** 코드의 `elif i == 'C':` 조건 블록 아래에서 `RNA` 변수에 더해지는 문자를 찾아보세요.

## Question 10
파이썬의 PIL 라이브러리로 새 이미지를 생성할 때 사용되는 `Image.new(self.img1.mode, self.img1.size, color = 'white')` 코드에 대한 설명으로 올바른 것은?

- [x] img1과 동일한 모드와 크기를 가진 흰색 바탕의 새 이미지 인스턴스를 생성한다.
- [ ] img1의 이미지를 흑백 모드로 전환하여 새로 저장한다.
- [ ] img1과 크기가 동일하지만 투명도가 적용된 배경 이미지를 생성한다.
- [ ] img1의 원본 이미지 위에 흰색 글씨를 덮어쓰는 작업을 수행한다.

**Hint:** 생성되는 인스턴스의 모드, 크기, 초기 색상 인자를 살펴 보세요.
