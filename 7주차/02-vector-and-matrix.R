# Vector의 작성
# C, seq, rep 함수로 작성
# 인덱스는 1부터 시작
# 단일 벡터는 단일 자료형만 저장
# 결측치는 NA로 표기
v <- c(1,2,3,4,5,6,7,8,9,NA)
v

# 통계 함수의 적용
mean(v) # NA 포함된 벡터의 연산은 NA
# NA 제거한 나머지 수치의 연산 na.rm = T
mean(v, na.rm=TRUE) # 5

# seq 함수
seq(1,10,3) # 1부터 10까지 3간격으로 증가하는 수
seq(from = 1, to = 10, by = 3)
seq(to=10, by=3, from=1) # 명명된 파라미터 순서는 중요하지 않다.
seq(from=1, to=100, length.out = 12) # 균등 분할

# rep 함수(반복)
rep(1:3, 3) # 1~3까지의 수열을 3번 반복
rep(c(1,3,5), 2) # 1,3,5 수열을 2번 반복
rep(c(1,3,5), each=3) # 개별 요소를 each개만큼 반복

# 인덱스
vec <- c(6,1,3,2,6,10,11)
# R의 인덱싱인 1부터 시작
vec[1] # 6 # 첫번째 요소
length(vec) # 7
vec[length(vec)] # 11 # 가장 마지막 요소

vec[8] # 인덱스를 벗어나면 NA 반환
# 특정 인덱스 요소를 추출하고자 한다 : 슬라이싱
vec[c(1,3,5,7)] # [1]  6  3  6 11 # 지정된 인덱스의 요소 벡터 반환
vec[c(-1,-3,-5,-7)] # [1]  1  2 10 # 지정된 인덱스 제외 요소 벡터 반환환

incomes <- seq(1500, 4000, length.out = 12)
incomes

incomes[2:7] # 2~7 인덱스 구간을 슬라이싱
# incomes에서 2500을 초과하는 비교연산
incomes[incomes > 2500]


# 벡터 이름의 벡터 확인
scores <- c(90, 80, 85)
names(scores) <- c("ENG", "MATH", "SCIENCE")
scores
# 요소에 이름 부여하면 이름으로 요소에 접근 가능
scores['ENG']


# 벡터 관련 함수들
x <- seq(1,12,by=2)
x
y <- seq(2,7)
y

cor(x,y) # 상관 계수 : 1에 가까울수록 양의 상관 관계
rev(x)
cor(rev(x), y) # 음의 상관관계
sd(x) # 표준편차
var(x) # 분산

summary(x) # x의 통계량 요약
summary(x)["3rd Qu."]

quantile(x) # 4분위수 추출

# 벡터의 연산
v <- seq(1,10) # [1]  1  2  3  4  5  6  7  8  9 10
v

# 벡터와 스칼라의 연산
# Broadcasting
v + 2 # [1]  3  4  5  6  7  8  9 10 11 12

# 벡터와 벡터의 연산
v1 <- c(1,3,5)
v2 <- c(2,3,6)

v1 + v2 # 벡터의 같은 위치에 있는 요소들이 개별연산
v1 == v2 # 벡터의 비교(논리) 연산 -> 논리벡터

# 논리 벡터를 이용하여 필요한 요소를 추출
# Fancy Indexing
# 벡터로 인덱싱 할 때 TRUE, FALSE 논리값으로 요소 추출
v1[c(TRUE, FALSE, TRUE)]

c <- seq(1,10)
c

# 벡터 c에서 짝수만 추출하고자 할 경우
x <- c(1:10)
x[x%%2==0]


# Matrix
# 모양이 다른 Vector로 취급
# 벡터의 특징과 벡터 함수가 그대로 사용

# c, seq, rep 등으로 벡터를 만들어 데이터로 사용
m1 <- matrix(1:10, ncol=2) # 1~10 벡터, 컬럼수 2
m1

m2 <- matrix(1:10, nrow=2, byrow=T) # 1~10 벡터, 행수 2, 행기준으로 채움
m2

m3 <- matrix(1:10, ncol=3, byrow=T)
m3 # 갯수가 맞지 않을 경우, 순환 규칙에 따라 채움

# 행렬의 인덱스 Row 인덱스, col 인덱스
m1[3,2]

# 행렬의 행과 열에 이름 붙이기
# colnames(), rownames()
m1
colnames(m1) # NULL
colnames(m1) <- paste0("C", 1:2)
rownames(m1) <- paste0("R", 1:5)

colnames(m1)
rownames(m1)
m1

# 길이
length(m1) # 10 # 내부 벡터의 길이
nrow(m1) # 5 # 메트릭스의 행 수
ncol(m1) # 2 # 메트릭스의 열 수

dim(m1) # 5 2 # 차원의 개수

# 슬라이싱
# 행인덱스 범위, 열인덱스 범위를 지정
m1

m1[2:3, 1:2]
m1[2:3,] # 범위를 생략하면 해당 범위 전체
m1[,1]
m1[,] # 메트릭스 전체

# 행렬의 연산
x <- matrix(1:4, ncol=2, byrow=FALSE)
x
y <- matrix(1:4, ncol=2, byrow=TRUE)
y

x + y
x * y

# 선형대수 행렬 곱의 연산자는 %*%로 사용
x %*% y

# 매트릭스의 주요 함수들
sum(x) # 벡터의 함수 -> 데이터 전체를 대상으로 함
mean(x) # 벡터의 함수

colSums(x) # 열의 합계 벡터
rowSums(x) # 행의 합계 벡터
colMeans(x) # 열의 평균 벡터
rowMeans(x) # 행의 평균 벡터

m1 # 5행 2열의 벡터
dim(m1) # [1] 5 2

# 전치 행렬 : 행 <-> 열
t(m1)

# cbind(열 기준으로 행렬 연결), rbind(행기준으로 행렬 연결)
# 주의 : 기준에 맞는 행, 열의 갯수가 일치해야 한다.
m1 

m4 <- matrix(1:4, ncol=2)
m4

# 행 기준으로 매트릭스 연결
rbind(m1, m4)
# 열 기준으로 매트릭스 연결
cbind(t(m1), m4)

# apply
# 행렬에서 행기준, 혹은 열기준으로 계산 함수를 적용하고자 할 경우 사용
# MARGIN == 1 : 행기준
# MARGIN == 2 : 열기준
scores <- matrix(c(80,90,70,65,75,90,80,70,85), ncol = 3)
scores
rownames(scores) <- paste0("R", 1:3)
colnames(scores) <- paste0("C", 1:3)
scores

apply(scores, 1, median) # 행기준으로 median 함수를 적용
apply(scores, MARGIN=2, FUN=median) # 열기준으로 중앙값 적용
apply(scores, FUN=summary, MARGIN = 1)







