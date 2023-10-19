# -*- coding: utf8 -*-
# coder:nianboy
# time:2022-9-14
import time

import requests
import re
import datetime
from Crypto.Hash import MD5


class ChaoXing:
    def __init__(self):
        self.headers = {
            "Host": "office.chaoxing.com",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "cors",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (schild:c36c66993fe8fbb1106a5ae711511e9c) (device:iPhone13,3) Language/zh-Hans com.ssreader.ChaoXingStudy/ChaoXingStudy_3_6.2.1_ios_phone_202308041130_115 (@Kalimdor)_3575081080828352536",
            "Connection": "keep-alive",
            # "Referer": "https://office.chaoxing.com/front/apps/seat/select?id=5950&day=2023-08-21&backLevel=2&pageToken=85c1b874b74347e790efd3fc732f61c3",
            "Cookie": "JSESSIONID=137831F033528DCBC699172279D8DDAE.reserve_web_124; oa_deptid=29397; oa_enc=bb00354a96a43848cc5a4a49d457e1b0; oa_name=%E9%BB%84%E9%B9%8F; oa_uid=141300358; route=3b84754f32aaf54a995f7d41f1a28848; DSSTASH_LOG=C_38-UN_1604-US_141300358-T_1692601005413; KI4SO_SERVER_EC=RERFSWdRQWdsckNwckxwM2pXeFFSWU5uU1NKZ2t3T005RUZYTk9TaUxhYlNnTDU0SlZkcjg4cTNI%0AMjVWV01FSkRtU2djWlRjU2NTVQp1NG13bWtscWxRWlBUMGxpN1EyV3M4RG55NDNtMStNN3dlclJt%0ARDFtdWE0OVd4bXBHSTZoQ1dxczczNElsTkhpWEtldW1sQVZrVWxPCjhKbkRyZHlUbWN4aERUOFhS%0AT0l4T2c5LzMxYzFNL05OU3pNajNvY29hcU12bVBycExsckV6TWJLYkEvdFhVaTgwMTYzRHRKZUd2%0ARUgKaW55cFE3ZW1aNW9oUGRsVWp6SHVORHFmVXE1ZDR5dzJsQTZ4bXp1YkFhQ1ovdW5NNy9TZWhn%0AcDFVZFJMTWU0ME9wOVNybDM0ZjZ5awovQUZtNzdqR01sZzcrM2tqQWhOb1g1Q0hiQmt4N2pRNm4x%0AS3VYY0x2d0lRNUVwZFlIdThhdXdNQzl1b1kvNFc5aWFwbGxUSHVORHFmClVxNWQrSCtzcFB3Qlp1%0AKzR4akpZTy90NUk2MERlVllabCtxZko4Y1N1WDEyWExlcGRMYmxFdDE0ZlZscmNuenpBcWZkU3NY%0Ac01DVTIKbzFJPT9hcHBJZD0xJmtleUlkPTE%3D; UID=141300358; _d=1692601005411; _industry=5; _tid=100266765; _uid=141300358; cx_p_token=731d31f2097331afac459fe10a012f18; fid=1427; fidsCount=2; lv=1; sso_puid=141300358; uf=b2d2c93beefa90dcd583ce2baf4b0f3bab1db1a4db93679d4461ff6154a9705046812db39e570f2f42646683e2e5ad9e913b662843f1f4ad6d92e371d7fdf6440fd631a2053cb2f98b6f06f3c6e4d776db9a01fd759e1b98be5b09e915e50dbcd36f935d31af5b51; vc=A66EACD032893C3EDA0476C3A3995E9E; vc2=84FFE2AF42939A95ABD0F9652533838D; vc3=UJYpCEULxs6IQWIv1KkOaaCZA3yWuATD%2FE4UIwDkfD9FwxWrojXnXWJwr18kWN6lEheKgz7lO%2FHp0PdidJW3f5GzDomY2gZAAuZBG53kso7lntgMJxiQhEm2u55aKvQdAedyhQiTeMRL5JTvVIFuc%2BCCl8vuDJRSUXFPI2pzUGY%3D2f2652f710411aaaf2fbd78efe6af630; xxtenc=c7077e51a359852bdb40c5aecc0f13a2; source=num99; spaceFid=29397; wfwEnc=868A996A2F4C133D27191A235F8A3855; wfwIncode=lib1118; wfwfid=29397",
            "Sec-Fetch-Dest": "empty"
        }
        self.session = requests.session()
        self.pageToken = ''
        self.token = ''
        self.seat_list_url = "http://office.chaoxing.com/front/third/apps/seat/list?deptIdEnc=cb783d1327681137"

    def updateDay(self):
        print("updateDay")
        today = datetime.datetime.now()
        self.today_time = today.strftime("%Y-%m-%d")
        self.tomorrow_time = (today + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        self.day = self.tomorrow_time

    def getEnc(self, today, endTime, seatNum, startTime, token):
        # "[captcha=][day=2023-06-03][endTime=19:00][roomId=1901][seatNum=022][startTime=18:30][token=xxx][%sd`~7^/>N4!Q#){'']"
        content = "[captcha=][day={}][endTime={}][roomId=5950][seatNum={}][startTime={}][token={}][%sd`~7^/>N4!Q#){}'']".format(
            today, endTime, seatNum, startTime, token, "{")
        result = MD5.new()
        result.update(content.encode('utf-8'))
        return result.hexdigest()

    def login(self, name='17863525054', pwd='hp160613'):
        print("login")
        login_api = "https://passport2.chaoxing.com/api/login"
        params = {
            "name": name,  # 学习通账号
            "pwd": pwd,  # 学习通密码
            "verify": "0",
            "schoolid": "",
        }
        self.session.get(login_api, params=params, headers=self.headers)
        page_resp = self.session.get(url=self.seat_list_url, headers=self.headers).text
        self.pageToken = re.findall(r"'&pageToken='.*?'(.*?)'", page_resp)[0]
        seat_select_url = (
                "https://office.chaoxing.com/front/third/apps/seat/select?id=" + str(
            id) + "&day=" + self.day + "&backLevel=2&pageToken=" + str(
            self.pageToken) + "&fidEnc=cb783d1327681137"
        )
        seat_select_res = self.session.get(url=seat_select_url, headers=self.headers).text
        self.token = re.findall(r"token = '(.*?)'", seat_select_res)[0]
    def book_seat(self, seatId="014", id="5950", start_time="21:00", end_time="22:00"):
        b_res = False
        seat_submit_url = (
            "https://office.chaoxing.com/data/apps/seat/submit?roomId={}&startTime={}&endTime={}&day={}&seatNum={}"
            "&captcha=&token={}&enc={}".format(
                str(id), start_time, end_time, self.day, str(seatId), str(self.token),
                self.getEnc(self.day, end_time, str(seatId), start_time, str(self.token)))
        )
        print("url:", seat_submit_url)
        page_text = self.session.get(url=seat_submit_url, headers=self.headers).text
        print("page_text", page_text)
        if '"success":true' in page_text:
            print("预约成功！")
            b_res = True
        else:
            print(page_text + "预约失败！")
        return b_res


if __name__ == "__main__":
    chaoxing = ChaoXing()  # 座位号
    seat_list = ["014", "015", "016", "017", "018", "002", "003", "004", "005", "006", "007", "008", "009",
                 "010", "011", "013", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029",
                 "030", "031", "032", "033", "034", "035", "036"]
    b_get_seat_morning = b_get_seat_evening = False
    chaoxing.updateDay()
    print('chaoxing started, waiting for 19:00:00')
    print('#'*200)
    while True:
        t = datetime.datetime.now().strftime("%H:%M:%S")

        if t == "19:00:00":  # 指定时间抢
            time.sleep(0.4)
            print(datetime.datetime.now())
            for i_seat in seat_list:
                if not b_get_seat_evening:
                    if chaoxing.book_seat(seatId=i_seat, start_time="16:00", end_time="22:00"):
                        print(datetime.datetime.now())
                        b_get_seat_evening = True
                        chaoxing.login()
                if not b_get_seat_morning:
                    if chaoxing.book_seat(seatId=i_seat, start_time="10:00", end_time="16:00"):
                        print(datetime.datetime.now())
                        b_get_seat_morning = True
                        chaoxing.login()
            time.sleep(1)
            print('today done')
            print('#'*200)
        else:
            time.sleep(0.2)

        if t == "18:59:50":  # 指定时间登录
            chaoxing.login()
            b_get_seat_morning = b_get_seat_evening = False
            time.sleep(2)
        elif t == "00:00:00":
            chaoxing.updateDay()
    # id是room_id需要抓包，start_time是预约开始时间，end_time是结束预约时间，name是学习通账号，pwd是学习通密码
