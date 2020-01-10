def using_range():

    seq=range(10)
    print(seq,type(seq))
    print(list(seq))
    seq2=range(2,10)
    print(seq2,type(seq2))
    print(list(seq2))

    seq3=range(2,10,2)
    print(seq3,type(seq3))
    print(list(seq3))

    seq4=range(10,2,-1)
    print(seq4,type(seq4))
    print(list(seq4))
    for num in range(2,10):
        print(num)

def using_enumerate():
    colors=["red","yello","blue","green","orange"]

    for index,  color in enumerate(colors):
        print("{}-{}".format(index+1,color))

    nums=[3,6,1,7,4,2,9,0]

    for index,num in enumerate(nums):
        nums[index]=num*2

    print(nums)

def using_zip():
    english="sun","mon","tue","wed"
    korean="일","월","화","수","목"
    engkor=zip(english,korean)
    print(engkor,type(engkor))
    #zip은 1회 소비성 객체

    for pair in engkor:
        print(pair,type(pair))


    engkor=zip(english,korean)
    for eng,kor in engkor:
        print("{} {}".format(eng,kor))

    engkor=zip(english,korean)
    dct= dict(engkor)
    print(dct)
if __name__=="__main__":

    #using_range()
    #using_enumerate()
    using_zip()