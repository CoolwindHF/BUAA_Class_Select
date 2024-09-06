import requests
from bs4 import BeautifulSoup
import time 
from random import random

from requests.packages import urllib3

urllib3.disable_warnings()


class TokenOutOfTimeError(Exception):
    pass

def store_jsessionid(response):
    set_cookie = response.headers.get("Set-Cookie")
    if set_cookie is None:
        raise TokenOutOfTimeError
    jsessionid = set_cookie.split(";")[0].split("=")[1]
    with open('jsessionid', 'w') as f:
        f.write(jsessionid)

def get_jsessionid():
    with open('jsessionid', 'r') as f:
        return f.read().strip()

def now_time():
    return time.strftime("[%H:%M:%S]", time.localtime())

def login(id, passwd):
    
    def get_execution():
        cookies = {
            '_7da9a': 'http://10.0.3.60:8080',
        }

        headers = {
            'Host': 'sso.buaa.edu.cn',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Referer': 'https://byxt.buaa.edu.cn/',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        params = {
            'service': 'https://byxt.buaa.edu.cn/jwapp/sys/homeapp/index.do',
        }

        response = requests.get('https://sso.buaa.edu.cn/login', params=params, cookies=cookies, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        execution = soup.find('input', {'name': 'execution'}).get('value')
        # print(execution)
        return execution
    
    def get_castgc(id, passwd, execution):
        cookies = {
            '_7da9a': 'http://10.0.3.60:8080',
        }

        headers = {
            'Host': 'sso.buaa.edu.cn',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Accept-Language': 'zh-CN',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://sso.buaa.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://sso.buaa.edu.cn/login?service=https%3A%2F%2Fbyxt.buaa.edu.cn%2Fjwapp%2Fsys%2Fhomeapp%2Findex.do',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Priority': 'u=0, i',
            'Connection': 'keep-alive',
        }

        data = {
            'username': id,
            'password': passwd,
            'submit': '登录',
            'type': 'username_password',
            'execution': execution,
            '_eventId': 'submit',
        }

        response = requests.post('https://sso.buaa.edu.cn/login', cookies=cookies, headers=headers, data=data, verify=False, allow_redirects=False)
        # print(response.headers)
        CASTGC = response.headers.get('Set-Cookie').split(';')[0].split('=')[-1]
        # print(CASTGC)
        return CASTGC

    def get_location(CASTGC):
        cookies = {
            "_7da9a": "http://10.0.3.60:8080",
            "CASTGC": CASTGC,
        }

        headers = {
            "Host": "sso.buaa.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '""',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close",
        }

        params = {
            "service": "https://byxk.buaa.edu.cn/xsxk/auth/cas",
        }

        response = requests.get(
            "https://sso.buaa.edu.cn/login",
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
            allow_redirects=False,
        )
        # print(response.text)
        location = response.headers.get("Location").strip().split("=")[-1]
        return location
    
    def get_token(location):
        cookies = {
            "route": "c91e5166ffb236526014aa4180e7f1e5",
        }

        headers = {
            "Host": "byxk.buaa.edu.cn",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '""',
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Connection": "close",
        }

        params = {
            "ticket": location,
        }

        response = requests.get(
            "https://byxk.buaa.edu.cn/xsxk/auth/cas",
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
            allow_redirects=False,
            
        )
        # print(response.headers)
        store_jsessionid(response)
        # print(get_jsessionid())
        cookies["JSESSIONID"] = get_jsessionid()
        response = requests.get(
            "https://byxk.buaa.edu.cn/xsxk/auth/cas",
            cookies=cookies,
            headers=headers,
            verify=False,
            allow_redirects=False,
            
        )


        # print(response.headers)
        token = response.headers.get("Set-Cookie").strip().split(";")[0][6:]
        return token
    


    execution = get_execution()
    CASTGC = get_castgc(id, passwd, execution)
    location = get_location(CASTGC)
    token = get_token(location)
    with open("action.log","a") as log:
        log.write(now_time()+f"已登陆账号{id}"+"\n")
    print(now_time(), f"已登陆账号{id}")
    return token


class ClassInfo:
    def __init__(self, classType, classID):
        self.classType = classType
        self.classID = classID

classes = {}



def find_class_in_list(token, classType:int, classForFind:list):
    global classes

    type_dict = {
        0: "TJKC",
        1: "FANKC",
        2: "FAWKC",
        3: "CXKC",
        4: "YYKC",
        5: "TYKC",
        6: "XGKC",
        7: "KYKT"
    }
    

    cookies = {
        "token": token,
        "JSESSIONID": "",
        "route": "c91e5166ffb236526014aa4180e7f1e5",
        "Authorization": token,
    }

    headers = {
        "Host": "byxk.buaa.edu.cn",
        "Batchid": "84e54db53fde46689e23e69f2693a83d",
        "Sec-Ch-Ua-Mobile": "?0",
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua-Platform": '""',
        "Origin": "https://byxk.buaa.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://byxk.buaa.edu.cn/xsxk/elective/grablessons?batchId=84e54db53fde46689e23e69f2693a83d",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }

    def set_jsessionid():
        cookies["JSESSIONID"] = get_jsessionid()

    def check_repetition(classType, id):
        for _class in classes[classType]:
            if _class.classID == id:
                return True
        return False

    

    def find_class(classType:int, classForFind:list):
        set_jsessionid()
        
        json_data = {
            "teachingClassType": type_dict[classType],
            "pageNumber": 1,
            "pageSize": 999,
            "orderBy": "",
            "campus": "1",
            "SFCT": "0",
        }

        response = requests.post(
            "https://byxk.buaa.edu.cn/xsxk/elective/buaa/clazz/list",
            cookies=cookies,
            headers=headers,
            json=json_data,
            verify=False,
        )

        store_jsessionid(response)
        set_jsessionid()
        response_json = response.json()
        rows = response_json["data"]["rows"]
        
        for _class_for_find in classForFind:
            isFind = False
            for id, row in enumerate(rows):
                # print(row)
                if "SKSJ" not in row:
                    continue
                if row["SKSJ"][0]["KCM"] == _class_for_find or row["SKSJ"][0]["KCH"]== _class_for_find:
                    
                    if classType not in classes:
                        classes[classType] = []
                    elif check_repetition(classType, id):
                        continue
                    classes[classType].append(ClassInfo(type_dict[classType], id))
                    print(now_time(), "课程{}已加入选课队列".format(row["SKSJ"][0]["KCM"]))
                    isFind = True
                    break
            if not isFind:
                print(now_time(), "未找到课程{}，请重新输入".format(_class_for_find))
            
    
    find_class(classType, classForFind)
    


def select_class(token, studentClass):
    global classes

    type_dict = {
        0: "TJKC",
        1: "FANKC",
        2: "FAWKC",
        3: "CXKC",
        4: "YYKC",
        5: "TYKC",
        6: "XGKC"
    }
    

    cookies = {
        "token": token,
        "JSESSIONID": "",
        "route": "c91e5166ffb236526014aa4180e7f1e5",
        "Authorization": token,
    }

    headers = {
        "Host": "byxk.buaa.edu.cn",
        "Batchid": "84e54db53fde46689e23e69f2693a83d",
        "Sec-Ch-Ua-Mobile": "?0",
        "Authorization": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36",
        "Content-Type": "application/json;charset=UTF-8",
        "Accept": "application/json, text/plain, */*",
        "Sec-Ch-Ua-Platform": '""',
        "Origin": "https://byxk.buaa.edu.cn",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://byxk.buaa.edu.cn/xsxk/elective/grablessons?batchId=84e54db53fde46689e23e69f2693a83d",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }

    def set_jsessionid():
        cookies["JSESSIONID"] = get_jsessionid()


    def check_selectablility():
        set_jsessionid()
        json_data = {
            "teachingClassType": "",
            "pageNumber": 1,
            "pageSize": 999,
            "orderBy": "",
            "campus": "1",
            "SFCT": "0",
        }

        for key in classes:
            json_data["teachingClassType"] = type_dict[key]
            response = requests.post(
                "https://byxk.buaa.edu.cn/xsxk/elective/buaa/clazz/list",
                cookies=cookies,
                headers=headers,
                json=json_data,
                verify=False,
            )
            store_jsessionid(response)
            set_jsessionid()
            response_json = response.json()
            rows = response_json["data"]["rows"]
            for i, _class in enumerate(classes[key]):
                class_in_rows = rows[_class.classID]
                try:
                    tjbj = class_in_rows["TJBJ"].split(",")
                except:
                    tjbj = []
                if studentClass not in tjbj:
                    capacity = class_in_rows["externalCapacity"]
                    selected = class_in_rows["externalSelectedNum"]
                else:
                    capacity = class_in_rows["internalCapacity"]
                    selected = class_in_rows["internalSelectedNum"]
                
                if capacity > selected:
                    with open("action.log","a") as log:
                        log.write(now_time()+f"课程{class_in_rows['SKSJ'][0]['KCM']}人数为{selected}/{capacity} 可选"+"\n")
                    print(now_time(), f"课程{class_in_rows['SKSJ'][0]['KCM']}人数为{selected}/{capacity} 可选")
                    jxbid = class_in_rows["JXBID"]
                    secretVal = class_in_rows["secretVal"]
                    if select_class(type_dict[key], jxbid, secretVal):
                        classes[key].pop(i)
                        with open("action.log","a") as log:
                            log.write(now_time()+f"课程{class_in_rows['SKSJ'][0]['KCM']}已选"+"\n")
                        print(now_time(), f"课程{class_in_rows['SKSJ'][0]['KCM']}已选")
                    else:
                        with open("action.log","a") as log:
                            log.write(now_time()+f"课程{class_in_rows['SKSJ'][0]['KCM']}选课失败"+"\n")
                        print(now_time(), f"课程{class_in_rows['SKSJ'][0]['KCM']}选课失败")
                else:
                    print(now_time() ,f"课程{class_in_rows['SKSJ'][0]['KCM']}人数为{selected}/{capacity} 不可选")
        
        len_0_list = []
        for key in classes:
            if len(classes[key]) == 0:
                len_0_list.append(key)
        for key in len_0_list:
            classes.pop(key)

    def select_class(classType, jxbid, secretVal):
        set_jsessionid()
        now_headers = headers.copy()
        now_headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = {
            "clazzType": classType,
            "clazzId": jxbid,
            "secretVal": secretVal,
        }
        # print(data)
        response = requests.post(
            "https://byxk.buaa.edu.cn/xsxk/elective/buaa/clazz/add",
            cookies=cookies,
            headers=now_headers,
            data=data,
            verify=False,
        )
        store_jsessionid(response)
        set_jsessionid()
        response_json = response.json()
        # print(response_json)
        if response_json["code"] == 200:
            return True
        else:
            return False
        
    check_selectablility()
    


if __name__ == '__main__':
    print("欢迎使用北航选课助手，本程序用于解决流量高峰时选课网站前端无法加载的问题")
    print("选课期间无法登陆选课系统，如需登陆请结束本程序")
    print("【作者声明：本程序仅用于学习交流，不得用于任何商业用途，否则后果自负】")
    print("Author Coolwind")
    open("action.log", "w").close()
    id = input("请输入统一认证学号：").strip()
    passwd = input("请输入统一认证密码：").strip()
    token = login(id, passwd)
    student_class = input("请输入学生班级：").strip()
    while True:
        classType = input("请输入课程类型代号，或输入[h]查看课程类型代号对应关系，将所有课程填写结束后输入[y]进行选课\n").strip()
        if classType == "h":
            print("0: 班级推荐课程")
            print("1: 方案内课程")
            print("2: 方案外课程")
            print("3: 重修课程")
            print("4: 英语课")
            print("5: 体育课")
            print("6: 通识选修课")
        elif classType == "y":
            break
        else:
            classType = int(classType)
            classForFind = input("请输入要选择的【课程完整名称】或者【课程代码】，使用【空格】分隔：\n").strip().split()
            find_class_in_list(token, classType, classForFind)

    
    while True:
        time.sleep(0.5+random())
        try:
            select_class(token, student_class)
            if len(classes) == 0:
                with open("action.log","a") as log:
                    log.write(now_time()+"选课结束"+"\n")
                print(now_time(), "选课结束")
                break
        except TokenOutOfTimeError:
            print(now_time(), "Token过期，重新登录")
            with open("action.log","a") as log:
                log.write(now_time()+"Token过期，重新登录"+"\n")
            time.sleep(10)
            token = login(id, passwd)
