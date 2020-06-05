from operator import eq
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import pymysql
import time


def Main():
    # Driver Load
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    # driver = webdriver.Chrome("‪D:\\python\\lib\\chromedriver.exe", options=options)
    driver.implicitly_wait(3)
    #// *[ @ id = "ui-datepicker-div"] / div[1] / div / select[1] / option[2]
    driver.get("https://aglook.krei.re.kr/jsp/pc/front/trend/wholesaleTrend.jsp")
    # 캘린더이미지클릭
    # 이미지클릭후 날짜선택

    # 년도[10], [11], [12] -> 18, 19, 20
    yearlist = 12 # 2,3,4,5,6,8,9,10,11,12
    monthlist = [6]# 1,2,3,4,5,6,7,8,9,10,11,12

    #for year in yearlist:
    for month in monthlist:
            # 2019,01 -> 11,1 전달
    #if year == 12 and month == 6:
        year_month_click(driver, 12, month)

    # year_month_click(driver, 12, 4)
    driver.close()


def year_month_click(driver, m_year, m_month):
    for idx in range(1, 6):
        # 날짜는 1부터 31일 까지
        # 캘린더 이미지클릭
        driver.find_element_by_xpath('//*[@id="trendFrm"]/img').click()
        driver.implicitly_wait(20)

        time.sleep(1)
        # 매개변수 + 해서처리한다고하지만 날짜는 어쩌지;;;
        # 년도 클릭
        driver.find_element_by_xpath(
            '//*[@id="ui-datepicker-div"]/div[1]/div/select[1]/option[' + str(m_year) + ']').click()
        driver.implicitly_wait(20)
        time.sleep(1)# 월 [1] -> 1
        driver.find_element_by_xpath(
            '//*[@id="ui-datepicker-div"]/div[1]/div/select[2]/option[' + str(m_month) + ']').click()
        driver.implicitly_wait(20)
        time.sleep(1)
        # 월클릭한다음에 날짜리스트 화
        date_all_list = driver.find_elements(By.CLASS_NAME, 'ui-state-default')
        # 리스트화한날짜가 오늘날짜인지 검사 해서 True False Return
        # 오늘 날짜이면 False Return

        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%m-%d").strip()
        today_day = timestampStr[8:10]
        today_month = timestampStr[6:7]
        m_month = str(m_month)

        for date in date_all_list:
            # a tag 이고 , 조회한 Day 와 동일하다면
            if date.tag_name == 'a' and eq(date.text, str(idx)):
                # 오늘 날짜이면 return false
                # 2020229
                print(date.text)
                print(today_day)
                if m_year == 12 and eq(m_month, today_month) and int(date.text) == int(today_day)+1:

                    print("today+1 -> break")
                    return
                # 20200228
                elif m_year == 11 and eq(m_month, '2') and idx > 29:
                    print("마지막날")
                    print(date.text)
                    print(idx)
                    date.send_keys(Keys.ENTER)
                    driver.implicitly_wait(20)
                    time.sleep(1)

                # 20200229
                elif m_year == 12 and eq(m_month, '2') and idx > 30:
                    print("마지막날")
                    print(date.text)
                    print(idx)
                    print("마지막날")
                    date.send_keys(Keys.ENTER)
                    driver.implicitly_wait(20)
                    time.sleep(1)

                # elif eq(m_month, '4') or eq(m_month, '6') or eq(m_month, '9') or eq(m_month, '11') and idx > 31:
                # print("마지막날")
                # print(date.text)
                # print(idx)
                # date.send_keys(Keys.ENTER)

                else:
                    # 해당 캘린더 날짜 클릭 후 Return true
                    date.send_keys(Keys.ENTER)
                    driver.implicitly_wait(20)
                    time.sleep(1)

        # 검색 버튼
        driver.find_element_by_xpath('//*[@id="trendFrm"]/input[2]').send_keys(Keys.ENTER)
        # 검색후에  BeautifulSoup 생성
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 작성된 날짜  Get
        pageDate = (soup.find('input').get('value', str))
        # 페이지내에 있는 내용 Get
        finance_html = soup.select('table', {'class': 'sub_table_original mg_b45 '})[0]
        # 내용 유무 Check
        if (len(finance_html.select('tbody tr'))) > 2:
            # DB WRITE 포함
            # 페이지에 있는 내용, 작성된 날짜
            StartPageParsing(finance_html, pageDate)

        else:
            print((len(finance_html.select('tbody tr'))))
            print("없는페이지생략")
        # time.sleep(5)
        driver.implicitly_wait(3)


# 페이지내에이있는 항목긁기
def StartPageParsing(finance_html, pageDate):
    global curs
    conn = pymysql.connect(host='192.168.1.23', user='root', password='1231',
                               db='bms_test', charset='utf8')
    curs = conn.cursor()
    for item in finance_html.select('tbody tr '):
        품목 = item.select('tbody tr td')[0].text
        단위 = item.select('tbody tr td')[1].text
        전년평균 = item.select('tbody tr td')[2].text
        전년동월평균 = item.select('tbody tr td')[3].text
        전월평균 = item.select('tbody tr td')[4].text
        전일 = item.select('tbody tr td')[5].text
        당일 = item.select('tbody tr td')[6].text
        전년평균대비 = item.select('tbody tr td')[7].text
        전년동월대비 = item.select('tbody tr td')[8].text
        전월평균대비 = item.select('tbody tr td')[9].text
        전일대비 = item.select('tbody tr td')[10].text
        DBdata = (품목, 단위, 전년평균, 전년동월평균, 전월평균, 전일, 당일, 전년평균대비,
                  전년동월대비, 전월평균대비, 전일대비, pageDate)

        sql = """insert into """ + \
              """tbl_item(품목,단위,전년평균,전년동월평균,전월평균,전일,당일,전년평균대비,전년동월대비,""" + \
              """전월평균대비,전일대비,date)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        print(DBdata)
        curs.execute(sql, DBdata)
        conn.commit()


if __name__ == "__main__":
    Main()

    # print(pageDate)
    # print(type(pageDate))

    # print(soup.find('input').get('value', str))

# sql = """insert into """ + \
#              """tbl_item(itemNAME,unit,previousyear,LastyearAverage,MonthlyAverage,previousDay,Today,
#        previousyearprepare,Lastyearprepare,""" + \
#              """Monthlyaverageprepare,Thedaybeforeprepare,pagedate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
