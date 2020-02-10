import pymysql
import pandas as pd
from surprise import Reader
from surprise import Dataset
from surprise import SVD


def load_data():
    print("======= data loading start ===========")
    conn = pymysql.connect(host='192.168.1.5', user='root', password='1231',
                           db='movie_test', charset='utf8')
    curs = conn.cursor()
    sql = """SELECT title, score, NAME2 from m_score"""
    curs.execute(sql)
    rows = curs.fetchall()
    print("{}개의 데이터 로딩".format(len(rows)))
    print("======= data loading finish ===========")
    print()
    print()
    return rows


def data_preprocessing(data):
    print("======= data preprocessing start ========")

    # 데이터 전처리
    df = pd.DataFrame(data, columns=['title', 'score', 'NAME2'])
    df['NAME2'] = df['NAME2'].apply(lambda x: x[:3])
    df = df.drop_duplicates(['title', 'NAME2'], keep='first')[['title', 'score', 'NAME2']]
    df.columns = ["movieId", "rating", "userId"]
    df = df[['userId', 'movieId', 'rating']]

    print("data shape : {}".format(df.shape))
    print("data sample")
    print(df.head(2))

    print("======= data preprocessing start ========")
    print()
    print()
    return df


def find_top_lst_movie(df, userid, movie_len):
    print("======= data preprocessing start ========")
    # 전체 영화 목록
    total_movie_list = set(df.movieId)
    # 유저가 본 영화 목록
    movie_list = df[df['userId'] == userid]['movieId']
    # 유저가 보지 않은 영화 목록
    find_movie_list = total_movie_list - set(movie_list)

    # 데이터 로드
    reader = Reader(rating_scale=(0.0, 10.0))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

    # 추천 행렬 분해 알고리즘으로 SVD객체를 생성하고 학습수행
    algo = SVD()
    train = data.build_full_trainset()
    algo.fit(train)

    pred = []
    for iid in total_movie_list:
        pred.append(algo.predict(userid, iid, verbose=False))

    result = pd.DataFrame([[i.uid, i.iid, i.est] for i in pred], columns=df.columns[:3])

    result.sort_values(by="rating", ascending=False, inplace=True)

    top_lst = []

    print("{}님에게 {}개의 영화 추천 목록".format(userid, movie_len))
    print("--------------------------------")
    print()
    print()

    for i in result.values:
        if len(top_lst) == movie_len:
            break
        if i[1] in find_movie_list:
            print("{}".format(i[1]))
            top_lst.append(i)


def predict_movie_ratings_by_user(df, userid):
    print("======== predict start ==========")
    # 전체 영화 목록
    total_movie_list = set(df.movieId)
    # 유저가 본 영화 목록
    movie_list = df[df['userId'] == userid]['movieId']
    # 유저가 보지 않은 영화 목록
    find_movie_list = total_movie_list - set(movie_list)

    # 데이터 로드
    reader = Reader(rating_scale=(0.0, 10.0))
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)

    # 추천 행렬 분해 알고리즘으로 SVD객체를 생성하고 학습수행
    algo = SVD()
    train = data.build_full_trainset()
    algo.fit(train)

    pred = []
    for iid in total_movie_list:
        pred.append(algo.predict(userid, iid, verbose=False))

    result = pd.DataFrame([[i.uid, i.iid, i.est] for i in pred], columns=df.columns[:3])

    result.sort_values(by="rating", ascending=False, inplace=True)

    print(result.shape)
    print("======== predict finish ==========")
    print()
    print()
    return result


def find_new_movie():
    print("========== find start ==========")
    movie_title = [name[0] for name in pd.read_csv('movie_title.csv', encoding='cp949', header=None).values]
    print("========= find finish ===========")
    print()
    print()
    return movie_title


def print_recommend_movies(result, cnt):
    if result.shape[1] == 3:
        print("======== print start ==========")
        print("\"{}\" 사용자에게 {}개의 최신 영화 추천 목록입니다.".format(result['userId'].iloc[0], cnt))
        print()
        temp = 1
        for i in result.values:
            print(i[1])
            if temp == cnt:
                break
            temp += 1
        print()
        print("======== print finish ========")
    else:
        print("======== print start ==========")
        print("사용자에게 {}개의 최신 영화 추천 목록입니다.".format(cnt))
        print()
        temp = 1
        for i in result.index:
            print(i)
            if temp == cnt:
                break
            temp += 1
        print()
        print("======== print finish ========")


def find_user(df, userid):
    return len(df[df['userId'] == userid])


def recommend_movies_by_user(df, userid, cnt):
    print("======== recommend start ==========")
    movie_title = find_new_movie()

    def func(data):
        if data in movie_title:
            return True
        return False

    def func1(data):
        if len(df[df['movieId'] == data]) > 10:
            return True
        return False

    if find_user(df, userid) == 0:
        print("{} 이라는 사용자는 존재하지 않습니다.".format(userid))
        print("다른 사용자들의 평점 높은 상위 {}개의 영화 입니다.".format(cnt))
        print("다소 시간이 걸림...")
        result = df[df['movieId'].apply(func)]

        result = result[result['movieId'].apply(func1)]

        result = result.groupby("movieId").mean().sort_values(by="rating", ascending=False)

        return result

    result = predict_movie_ratings_by_user(df, userid)

    result = result[result['movieId'].apply(func)]

    print("======== recommend finish ==========")
    print()
    print()
    return result


if __name__ == "__main__":
    # find_top_lst_movie(df, 'edw', 5)
    # predict_movie_ratings_by_user(df, 'edw')

    user_name = input("사용자 이름을 입력하세요 : ")
    cnt_num = int(input("몇개의 영화를 원하시나요 : "))

    data = load_data()
    df = data_preprocessing(data)
    # find_user(df, user_name)

    print_recommend_movies(recommend_movies_by_user(df, user_name, cnt_num), cnt_num)



