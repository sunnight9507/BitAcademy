# 데이터 불러오기, 내보내기

# CSV(쉼표로 구분된 데이터 파일), TSV(탭 문자로 구분)
# read.csv, read.table 함수로 import
# -> DataFrame으로 변환

thieves <- read.csv("thieves.txt",
                    fileEncoding = "utf-8") # 유니코드
thieves

# \t문자를 구분자로, header는 없음으로 설정
thieves <- read.csv("thieves.txt",
                    fileEncoding = "utf-8", # 유니코드
                    sep = "\t", # 구분자를 탭문자로
                    header = FALSE # 첫 행은 헤더가 아님
                    )

thieves

# 컬럼에 이름 붙이기 : names()
names(thieves) <- c("이름", "신장", "체중")
thieves

# 엑셀 파일 import 
# 외부 패키지 필요
install.packages("readxl")
# 라이브러리 로드
library(readxl)

# wstudents.xlsx를 로드
wstudents <- read_excel("wstudents.xlsx",
                        col_names = TRUE, # 첫 행을 컬럼명으로
                        sheet = 1 # 1번 시트를 import
                        )
wstudents

# 연습
# class_scores.csv 임포트
# 데이터 확인
# 데이터를 2학년(grade == 2) 데이터만 따로 분류
# rdata 파일로 저장
class_scores <- read.csv("class_scores.csv")
class_scores

# 데이터의 구조 확인
str(class_scores)

# grade는 명목 변수로 변경
class_scores$grade <- as.factor(class_scores$grade)
str(class_scores)

class_scores$grade == 2
class_scores.grade2 = class_scores[class_scores$grade==2,]

# class_scores.grade2 객체를 RData파일로 저장
save(class_scores.grade2, file="class_scores.grade2.rda")

# class_scres.grade2 객체 삭제
rm(class_scores.grade2)
class_scores.grade2

# 객체 복원 테스트 : load
load("class_scores.grade2.rda")
class_scores.grade2

# csv로 저장
write.csv(class_scores.grade2, "class_scores.grade2.csv")
# 행 번호는 제외하고 저장
write.csv(class_scores.grade2, "class_scores.grade2.csv", 
          row.names = FALSE)  #행 번호는 저장하지 않음

# EDA : 탐색적 데이터 분석
#   가지고 있는 데이터를 살펴보면서
#   알아내지 못한 가치가 있는지 확인하는 작업
# 기본적인 작업들
#   데이터의 전반적 구조 확인
#   데이터의 변수들
#   실제 데이터의 모습들

# 내장 데이터셋 mtcars
?mtcars

# 데이터의 차원 확인
dim(mtcars)
# 데이터의 구조
str(mtcars)

# 데이터의 앞 부분 확인 : head(기본값은 6)
head(mtcars)
head(mtcars, n=10) # 앞부분 10개 확인

# 데이터의 뒷 부분 확인 : tail
tail(mtcars)
tail(mtcars, n=10)

# 컬럼과 행의 이름 확인
colnames(mtcars)
rownames(mtcars)

# 요약 통계량의 확인 : summary
summary(mtcars)

# 특정 변수의 요약 통계량
summary(mtcars[c("mpg", "wt")])

# 중량(wt) 변수의 Boxplot
boxplot(mtcars$wt)

wt.median <- median(mtcars$wt)
wt.median

bp <- boxplot(mtcars$wt)$stat # 상자 그림 통계치를 추출
wt.1q <- bp[2]
wt.1q
wt.3q <- bp[4]
wt.3q

# IQR : 3사분위수 - 1사분위수
wt.iqr <- wt.3q - wt.1q
wt.iqr

wt.top_border <- wt.3q + wt.iqr * 1.5
wt.top_border

wt.bottom_border <- wt.1q - wt.iqr * 1.5
wt.bottom_border

# 극단치 데이터
wt.outliers <- mtcars$wt[mtcars$wt > wt.top_border] # 상단 극단치치
wt.outliers

# IQR 함수
IQR(mtcars$wt)