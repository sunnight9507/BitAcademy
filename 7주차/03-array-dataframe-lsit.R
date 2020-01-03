# Array
# 2차원 이상 n 차원의 데이터
# 데이터는 vector 생성으로, 차원 정보는 dim 옵션으로 부여
# array 객체의 차원 정보는 dim 함수로 확인
vec <- 1:18
vec

arr <- array(vec, dim=c(3,3,2)) # 3행 3열 2매트릭스의 배열
arr

# 배열 요소의 이름 dimnames
dimnames(arr) <- list(
  paste0("R",1:3),
  paste0("C",1:3),
  paste0("M",1:2)
)
arr

dim(arr)

name <- c("홍길동", "전우치", "임꺽정", "장길산")
height <- c(175,170,186,188)
weight <- c(73,66,88,90)
thieves <- data.frame(name, height, weight)
thieves

# 변수의 사용 $기호 활용
thieves$name

# 인덱싱, 슬라이싱 -> 벡터와 매트릭스에서 사용했던 방식 그대로 사용
thieves$height[2:3]

# 수치 함수를 적용시 슬라이싱을 적절히 해 줘야 한다.
colMeans(thieves[,2:3])

thieves
new.thieves <- data.frame(name = "일지매",
                          height = 176,
                          weight = 63)
# 행 기준으로 새 데이터 프레임 연결
# 주의 : 동일 컬럼 명이 포함되어 있어야 한다.
rbind(thieves, new.thieves)
thieves

bloodtypes <- data.frame(name=c("전우치", "임꺽정", "홍길동", "장길산"),
                         bloodtype=c("A","B","O","AB"))

# 열 기준으로 새 데이터 프레임 연결
cbind(thieves, bloodtypes)
# 행 수가 일치해야 한다.
# 특정 컬럼을 기준으로 합칠 경우 merge 사용
thieves <- merge(thieves, bloodtypes, by="name")
thieves

# 변수의 파생
# 원래 있던 변수를 기반으로 새로운 변수를 만들어 내는 것
# 이렇게 만들어진 새 변수를 파생변수라 한다.
# thieves의 height 변수, weight 변수에 bmi 공식을 적용해 새 변수 bmi 파생
thieves$bmi <- thieves$weight / (thieves$height / 100) ^ 2
thieves

# 리스트
# R언어의 가장 범용적인 데이터 포맷
# 모든 객체가 다 들어갈 수 있다.
lst <- list(name = "홍길동", # 문자열
            physical = c(176,74), # 벡터
            scores = data.frame(int=90, health=80) # 데이터 프레임
            )
lst

# 길이 구할 수 있다.
length(lst)
str(lst) # 데이터의 구조 확인

# 리스트의 원소 구하기
lst['scores']
lst[3]
lst$scores

obj <- lst['scores'] # 리스트로 반환
is(obj)

df <- lst[['scores']] # 내부 객체를 반환
is(df)

# lapply : 여러 요소에 함수를 동시 적용하기 위한 함수
# -> 반환값이 list
v1 <- 10:30
v2 <- 50:70

lst2 <- list(v1,v2)
lst2

lapply(lst2, median)

# sapply : 여러 요소에 함수를 적용하고 벡터를 반환
sapply(lst2, median)

# 질적 변수 : Factor
var1 <- c(1,2,3,2,1)
var1
var1 * 2

var2 <- factor(c(1,2,3,2,1))
var2

is.factor(var1) # FALSE
is.factor(var2) # TRUE

var2 * 2 # 수치로서의 의미가 아니라 구분을 위한 변수다.

# as.factor 함수로 기존 객체를 범주형으로 변경
var3 <- as.factor(var1)
var3

# ordered : 순서가 있는 명목형 변수
sizes <- ordered(c("medium", "small", "large", "huge", "small"),
                 levels=c("small", "medium", "large", "huge"))
sizes
# 레벨의 확인
levels(sizes)

# medium보다 큰 요소의 확인
sizes > "medium"
# 불린 추출
sizes[sizes > "medium"]