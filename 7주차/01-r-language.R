# 주석
1 + 2 # 3

# 사칙연산 : +, -, /, *
# 정수 나눗셈의 몫과 나머지 : %/%, %%
7 %/% 5; 7 %% 5 # 1,2

# 논리 연산 : T(TRUE), F(FALSE)
# 비교 연산 : ==, !=

# 논리 연산자 &(AND), |(OR), !(NOT)
7 == 5 & 8 > 7 # FALSE
!(7 == 5 & 8 > 7) # TRUE
(7 == 5 & 8 > 8) == FALSE # TRUE
(7 == 5 & 8 > 8) == F # TRUE

## 객체
# 할당 : 할당 방향에 따라서 <-, -> 기호를 사용
# 객체 명명 규칙 : 문자, 숫자, _, .
#   문자로 시작해야 한다.
#   대소문자 확실히 구분한다.
eng <- 90
80 -> math
# 기존 프로그래밍 언어처럼 = 이용 할당
total = eng + math
average <- total / 2

total; average # 170, 85

# 객체들의 목록 확인 ls()
ls() # "average" "eng"     "math"    "Math"    "total"  

# 객체의 살제 : rm()
rm(average)

"average" %in% ls() # FALSE

# Vector
# R은 기본적으로 수치데이터는 모두 numeric으로
# 단일 데이터도 Vector로 처리

v1 <- c(2,4,6,8,10)
v1 # [1]  2  4  6  8 10

# 범위값을 이용한 벡터 생성
v2 <- seq(1,10)
v2 # [1]  1  2  3  4  5  6  7  8  9 10

# by 옵션으로 간격값을 부여
v3 <- seq(2,10, by=2)
v3 # [1]  2  4  6  8 10

v4 <- 1:10
v4 # [1]  1  2  3  4  5  6  7  8  9 10

# 균등 분할
v5 <- seq(1,100, length.out = 12)
# 1~100까지의 범위를 12개의 구간으로 균등분할
v5 # [1] 1  10  19  28  37  46  55  64  73  82  91 100

# 함수의 도움말
help(seq)
?seq

# 벡터의 길이
v6 <- 10
# R은 기본적으로 데이터를 벡터로 취급
length(v6) # [1] 1

# 벡터는 한 가지 데이터만 담을 수 있다
# 여러 형태가 섞여 있는 경우, 한가지 형태로 통일
v7 <- c(1,2,3,"4",5)
v7 # [1] "1" "2" "3" "4" "5"

# 기본 자료형
# numeric / 기본적으로 실수형으로 판단
n <- 3.14
n2 <- 3

# integer
i <- 314L # 정수형으로 할당할 경우 L을 부여
i2 <- 3L

# 복소수 : 실수부 + 허수부(i)
cpx <- 2 + 3i

# 수치자료형 -> 산술연산이 가능

# 문자 자료형 : ""
s <- "r programming"

# Date 형 : 문자열처럼 취듭되나
# Date형으로 변환할 수 있다.
dt <- as.Date("2020-01-02")

# 객체의 자료형 확인 : is() 함수
vec <- c(1,2,3,4,5)
is(vec) # [1] "numeric" "vector" 

# 세부 데이터 타입을 확인 as.{type}() 함수
is.numeric(vec) # TRUE
is.vector(vec) # TRUE
is.integer(vec) # FALSE

# 객체의 형 변환 : as 계열 함수
vec2 <- as.integer(vec)
vec2 # [1] 1 2 3 4 5
is(vec2) # [1] "integer"  "double" "numeric" "vector" "data.frameRowLabels"
is.numeric(vec2)
is.integer(vec2)

# 특수 데이터 타입들
# NA : 결측치(Missing value)
scores <- c(90, 80, 100, NA, 75)
scores

is.na(scores) # [1] FALSE FALSE FALSE  TRUE FALSE
length(NA) # [1] 1

nval <- NULL
is.null(nval) # [1] TRUE
length(NULL) # [1] 0
# NULL은 길이도 없는 빈 객체이다.

# Finite, Infinite
is.finite(7) # 유한 값 : TRUE

div <- 7/0; div # [1] Inf
is.infinite(div) # [1] TRUE

# NaN : Not A Number - 수학적으로 해석 불가능
1 / 0 - 1 / 0 # [1] NaN

# NA, NULL, Inf, NaN
# 통계 함수에서 오류발생 혹은 잘못된 결과를 반환
# 통계 함수 적용 이전에 이들 값을 적절히 처리

# 내장 통계 함수
scores <- c(90, 80, 70, 95, 100)
scores

sum(scores) # [1] 435
mean(scores) # [1] 87

mean(scores) == sum(scores) / length(scores) # TRUE
median(scores) # 중앙값
min(scores); max(scores) # 최솟값, 최댓값

scores2 <- c(90, 80, NA, 95, 100)
mean(scores2) # NA
# 통계 함수 적응시 NA를 무시하고자 할 경우
mean(scores2, na.rm=T) # 91.25

# 문자열 함수
# 기본 출력 함수 : print()
print("HEllo")
print("Hello" + " R programming") # Error in "Hello" + " R programming" : 이항연산자에 수치가 아닌 인수입니다
# 문자열 연결을 위해서는 paste 함수, paste()함수 이용
paste("Hello", "R", "programming") # [1] "Hello R programming"
# paste 함수 : 벡터 자료형을 문자열로 변환 합치는 함수

# 구분자는 기본으로 공백문자
# 구분자 바꿀 경우, sep 옵션
paste("Hello","R",sep = ",") # [1] "Hello,R"
# paste0은 paste 함수에서 sep옵션을 제거한 함수
paste0("Hello","R","Programming") # [1] "HelloRProgramming"
paste0("A", c(1,2,3)) # [1] "A1" "A2" "A3"
paste("A", c(1,2,3), sep="") # [1] "A1" "A2" "A3"

# 기초 산술 함수
# round(반올림), floor(버림), ceiling(올림)
val <- 35.67
round(val) # 36
round(val, 1) # 35.7
round(val, -1) # 40

floor(val); ceiling(val) # 35 / 36

# 사용자 정의 함수
# function으로 정의하여 객체에 할당
stats <- function(x) {
  return (c(min(x), max(x), sum(x), mean(x), median(x)))
}

stats(scores) # [1]  70 100 435  87  90

# 패키지
# 추가 기능들을 꾸러미로 묶어둔 것(확장)

# 설치된 패키지의 확인
installed.packages()
# 패키지의 도움말 확인
library(help = "base")

# 패키지 설치
install.packages("ggplot2")

# 패키지 업데이트
update.packages("ggplot2")

# 패키지 사용시에는 로드해야 한다.
library(ggplot2)

x <- c("a", "b", "c", "d", "c", "b", "a")
?qplot
qplot(x) # ggplot2의 Quick plot 함수를 사용할 수 있다.

# 조건문 if ~ else
x <- 10L
# x > 0 면 양수, x < 0 음수, 그렇지 않으면 0을 출력하는 함수
check_positive <- function(x){
  if(x > 0){
    print(paste0(x, "는 양수입니다."))
  } else if(x < 0){
    print(paste0(x, "는 음수입니다."))
  } else{
    print("0입니다.")
  }
}

check_positive(1) # [1] "1는 양수입니다."
check_positive(0)
check_positive(-2)

# switch 문 : 조건식의 결괏값에 따른 분기
# default는 없다.
test_switch <- function(x){
  res <- switch(x,
                "1st case",
                "2nd case",
                "3rd case")
  return (res)
}

test_switch(1) # [1] "1st case"
test_switch(2)
test_switch(3)
test_switch(4) # NULL

# ifelse
# ifelse(조건문, 조건문이 참일 때의 값, 거짓일 때 반환값)
test_ifelse <- function(x) {
  paste("x는", ifelse(x > 0,
                     "양수입니다.",
                     ifelse(x < 0,
                            "음수입니다.",
                            "0입니다.")))
}

test_ifelse(10L)
test_ifelse(0L)
test_ifelse(-1L)