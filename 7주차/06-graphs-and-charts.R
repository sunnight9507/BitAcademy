# 산점도 그래프(scatter Plot)
# 두 개의 변수간의 상관 관계를 표시하는 그래프
mtcars

# wt(중량), mpg(연비) 상관관계를 확인
# 상관계수
cor(mtcars$wt, mtcars$mpg) # 역상관 관계
plot(mtcars$wt, mtcars$mpg,
     xlab = "차량 중량", # x축의 라벨
     ylab = "연비", # y축의 라벨
     main = "weights vs Mpg" # 차트의 제목
     )

?plot

# 산점도 매트릭스
# 여러 개의 변수간의 상관 관계를 일목요연하게 보여주는 그래프
pairs(data = mtcars, # 데이터
      ~wt+mpg+disp+cyl,
      main = "산점도 매트릭스")

# 파이차트
# 전체 데이터 중에서 해당 데이터의 기여도를 비율로 표시
midterm <- data.frame(grade = c("A","B","c","D"),
                      cnt = c(3,12,11,2))
pie(midterm$cnt, # 데이터터
    labels = midterm$grade, # 조각에 표시할 라벨
    radius = 1,
    # col = c("blue", "green", "yellow", "red") # 색상 팔레트
    # col = c("#0000FF", "#00FF00", "#FFFF00", "#FF0000") 16진수 색상
    col = rainbow(4),
    main = "Midterm Scores"
    )

# 응용 : 파이차트 라벨을 비율로 대체
# 응용2 : 범례(legend) 넣기

midterm$percent <- round(100 * midterm$cnt / sum(midterm$cnt), 1)
midterm$percent

pie(midterm$cnt, # 데이터
    labels = midterm$percent,
    col = rainbow(4), # 색상 팔레트
    main = "Midterm scores"
    )

# 범례 표시
legend("topright", # 범례의 위치
       legend=midterm$grade, # 범례에 사용될 라벨
       fill = rainbow(4))

# Bar Chart
rev <- sample(1:20, 6, rep = T) # rep = T -> 복원 추출 허용
barplot(rev)
names <- c("MAR","APR","MAY","JUN","JUL","AUG")
barplot(rev, # 데이터
        names.arg = names, # 항목 표시 이름
        xlab = "월", # x축 라벨
        ylab = "Revenue", # y축 라벨
        main = "Revenue Chart", # 차트 타이틀
        col = "blue", # 바의 색상
        border = "red" # 테두리 색상
        )

# barplot에 matrix를 전달하면 stacked Bar Chart 생성
rev2 <- sample(1:20, 18, rep=T)
rev2
rev2 <- matrix(rev2, byrow=T, nrow=3)
rev2

barplot(rev2,
        names.arg = names,
        xlab = "Month",
        ylab = "Revenue",
        col = c("green", "orange", "red"),
        main = "Stacked Bar Chart")

#범례 넣기
legend("topright", # 위치
       c("Part A", "Part B", "Part C"), # 각 스택의 이름
       fill=c("green", "orange", "red"))

# histogram
# 특정 구간에 데이터의 출연 빈도, 혹은 밀도로 표현
wstudents$height
hist(wstudents$height,
     main = "Height of wstudents", # 차트의 제목
     xlab = "Height", # x축 라벨
     col = "yellow", # 컬러 팔레트
     border = "red" # 테두리 색상
    )

# 확률 밀도 그래프
hist(wstudents$height,
     main = "Height of wstudents", # 차트의 제목
     xlab = "Height", # x축 라벨
     col = "yellow", # 컬러 팔레트
     border = "red", # 테두리 색상
     freq = F # 확률 밀도 그래프
)

stat <- hist(wstudents$height, freq = F)
stat

stat$density # 각 구간의 밀도
stat$breaks

# 확률 밀도 그래프의 경우
# 바 너비(구간의 크기)와 density를 곱한 합은 1이 된다.
sum(stat$density * 5)

# Line 그래프
# 점, 혹은 선그래프
v <- sample(10:20, 5, rep=T)
v

plot(v, type="p") # 점그래프
plot(v, type="l") # 선그래프
plot(v, type="o") # 점과선그래프

plot(v, type = "o",
     main = "Line Graph",
     xlab = "HORZ Label",
     ylab = "VERT Label",
     col = "blue")
# plot 그린 후 lines 함수, points 함수를 이용하면
# 기존 그래프 위에 추가 그래프를 덧그릴 수 있다.
v2 <- sample(10:20, 5, rep=T)
lines(v2,
      type="o",
      col="red")