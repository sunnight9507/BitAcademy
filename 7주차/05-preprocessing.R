# 데이터 전처리
# with dplyr
install.packages("dplyr")
library(dplyr)

# 데이터 준비
scores <- read.csv("class_scores.csv")
scores

str(scores)
summary(scores) # 요약 통계계
# head, tail 등을 이용 데이터를 살표보기기

# filter : 조건에 맞는 행을 선택 - WHERE 절과 비슷
# R 방식
# scores의 grade == 1인 레코드 선택
scores[scores$grade == 1,] # 기본 방식
filter(scores, grade == 1) # dplyr
head(filter(scores, grade==1)) # 타 함수와의 조합

# gender 가 F인 데이터만 선택
scores[scores$gender == 'F', ] # 기본 방식
filter(scores, gender == 'F') # dplyr

# 논리값의 조합
# scores에서 grade == 1이고 class == 'B'인 데이터
filter(scores, grade == 1 & class == 'B') # 논리곱곱

# select : 특정 변수의 추출 - SELECT
# Math, English, Writing 변수 추출
select(scores, Math, English, Writing)
# 특정 변수 배제 : - 기호
select(scores, -gender, -Stu_ID) # gender, Stu_ID 배제제
# 컬럼의 범위를 이용한 변수 추출 : 
select(scores, Math:Writing)

# filter와 select를 이용
# 성별이 F고 grade가 3인 관측치 선택
# Stu_ID와 Math:Writing까지의 변수 선택
select(
  filter(scores,
         gender == 'F' & grade == 3),
  c(Stu_ID, Math:Writing)
)

# 변수의 파생 : mutate
# scores 데이터에 Total, Avg 파생변수 추가
mutate(scores, 
       Total = Math + English + Science + Marketing + Writing,
       Avg = (Math + English + Science + Marketing + Writing)/5)


# 연습문제
temp.filtered <- filter(scores, gender == 'F' & grade == 1)
temp.mutated <- mutate(temp.filtered,
                       Total = Math + English + Science + Marketing + Writing,
                       Avg = (Math + English + Science + Marketing + Writing)/5)
scores.refined <- select(temp.mutated, -c(Math:Writing))
scores.refined

# 풀이 2
select(
  mutate(
    mutate(
      filter(scores, grade == 1 & gender == 'F'),
      Total = Math + English + Science + Marketing + Writing),
    Avg = Total / 5
  ),
  -c(Math:Writing)
)

# Chain Operator %>%
# 앞쪽의 출력을 뒤쪽 함수의 입력값으로 전달
scores.refined <- scores %>% # 입력 데이터셋
  filter(grade == 1 & gender == 'F') %>%
  mutate(Total = Math + English + Science + Marketing + Writing) %>%
  mutate(Avg = Total / 5) %>%
  select(-c(Math:Writing))
scores.refined

# mutate 함수 내에서 ifelse를 이용한 변수 파생
scores.result <- scores.refined %>%
  mutate(Result = ifelse(Avg >= 90,
                         "A",
                         ifelse(Avg >= 80,
                                "B",
                                ifelse(Avg >= 70,
                                       "C",
                                       ifelse(Avg >= 60,
                                              "D",
                                              "F")))))

scores.result
str(scores.result)

# scores.result$Result 변수는 순서형 변수가 될 수 있을 것
scores.result$Result <- ordered(scores.result$Result,
                                levels=c("F","D","C","B","A"))
str(scores.result)

head(scores.result)

# scores.result에서 c이상의 성적을 받은 학생들
# 성적의 역순으로 출력 : arrange 함수
# 역순 정렬 desc()

scores.result %>%
  filter(Result >= "C") %>% # C학점 이상
  arrange(desc(Avg)) # 평균의 역순 정렬

# summarise와 group_by
# scores 데이터 셋 Math 점수의 평균
scores %>% summarise(mean(Math))
scores %>% summarise(mean.math = mean(Math),
                     mean.english = mean(English),
                     mean.writing = mean(Writing))

# group_by : 특정 조건으로 데이터를 그룹화
scores.group <- scores %>%
  group_by(grade, class)

scores.group %>% head(10)

# 반별 총점 평균 구하기
scores.group <- scores %>%
  group_by(grade, class) %>% # 그룹핑
  mutate(Total = Math + English + Science + Marketing + Writing) %>%
  mutate(Avg = Total / 5) %>%
  summarise(sum_tot = sum(Total), mean_tot = mean(Total)) %>%
  arrange(desc(mean_tot))

scores.group

# 결측치, 이상치
# 결측치가 포함된 데이터를 산술 연산하면 NA
library(ggplot2)
?mpg

str(mpg)

# mpg의 hwy 변수를 상자 그림으로 확인
bp <- boxplot(mpg$hwy)
bp$stats

# mpg의 hwy 변수의 정상 범주 12~37이다.
mileage <- mpg %>% select(cyl, cty, hwy)
mileage

# 극단치를 확인
outliers <- mileage %>%
  filter(hwy < 12 | hwy > 37)
outliers

# 극단치를 결측치로 대체
mileage$hwy <- ifelse(mileage$hwy < 12 | mileage > 37,
                      NA,
                      mileage$hwy)
mileage$hwy

# mileage$hwy 평균 확인
mean(mileage$hwy, na.rm = T) # 결측치를 배제한 산술평균

# 결측치가 많아도 통계 결과를 왜곡할 수 있다.
# 대푯값으로 NA를 대체해 줘야 한다.
hwy.med <- median(mileage$hwy, na.rm = T)
hwy.med

mileage$hwy <- ifelse(is.na(mileage$hwy),
                      hwy.med,
                      mileage$hwy)

# 최종 연비의 평균
mean(mileage$hwy)



