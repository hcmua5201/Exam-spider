from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import config
import time

app = Flask(__name__)
CORS(app)


@app.route('/login', methods=['get'])
def get_login():
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://www.wancode.net',
        'Referer': 'http://www.wancode.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }

    json_data = {
        'loginAccount': config.login_username,
        'password': config.login_password,
    }

    response = requests.post('http://www.wancode.net:8010/wancode/exam/user/login', headers=headers, json=json_data,
                             verify=False)
    print(response.text)
    return jsonify(response.json())


# 获取cookie
@app.route('/getCookie', methods=['get'])
def get_cookie():
    # edge_path = 'D:/PyCharm/Study/selenium学习自动化/msedgedriver.exe'

    driver = webdriver.Edge()

    # 打开网页
    url = "http://www.wancode.net/#/testPaperCenter"
    driver.get(url)

    # 等待页面加载完成
    time.sleep(2)

    # 定位登录按钮
    Login_diago = driver.find_element(By.CSS_SELECTOR,
                                      '#app > div:nth-child(1) > div:nth-child(1) > ul > li:nth-child(11) > div > button')
    Login_diago.click()

    # 定位用户名输入框并输入用户名
    username_input = driver.find_element(by="name", value="username")
    username_input.send_keys(config.login_username)

    # 定位密码输入框并输入密码
    password_input = driver.find_element(By.XPATH, '//*[@id="pane-login"]/div/div/div/form/div[3]/div/div/div/input')
    password_input.send_keys(config.login_password)

    # 点击登录按钮
    login_button = driver.find_element(By.CSS_SELECTOR, '#pane-login > div > div > div > form > button')
    login_button.click()

    # 等待登录完成
    time.sleep(1)

    # 获取Cookies
    cookies = driver.get_cookies()
    # 封装data
    data = {
        "JSESSIONID": cookies[0]['value'],
    }
    print('登陆之后获取cookies是' + str(data))


    return jsonify(cookies)



# 查询全部书籍信息
@app.route('/getAll', methods=['get'])
def FindAll():
    # 获取params
    currentPage = request.args.get('currentPage')
    type = request.args.get('type')
    level = request.args.get('level')
    token = request.args.get('token')
    JSESSIONID = request.args.get('JSESSIONID')
    print(currentPage, type, level, token)
    # 获取所有数据
    cookies = {
        'JSESSIONID': JSESSIONID,
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # 'Cookie': 'JSESSIONID=exam_login_token_b7978d87-e571-4db9-92b3-15f483611deb',
        'Origin': 'http://www.wancode.net',
        'Referer': 'http://www.wancode.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'token': token,
    }
    json_data = {
        'type': type,
        'level': level,
        'name': '',
        'currentPage': currentPage,
        'pageSize': 9,
    }
    response = requests.post(
        'http://www.wancode.net:8010/wancode/exam/paper/pageList',
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    print(response.text)
    return jsonify(response.json())


@app.route('/download', methods=['get'])
def download():
    token = request.args.get('token')
    id = request.args.get('id')
    name = request.args.get('name')
    JSESSIONID = request.args.get('JSESSIONID')
    cookies = {
        'JSESSIONID': JSESSIONID,
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        # 'Content-Length': '0',
        # 'Cookie': 'JSESSIONID=exam_login_token_b7978d87-e571-4db9-92b3-15f483611deb',
        'Origin': 'http://www.wancode.net',
        'Referer': 'http://www.wancode.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'token': token, }
    response = requests.get(
        'http://www.wancode.net:8010/wancode/exam/pdf/toDownload/' + id,
        cookies=cookies,
        headers=headers,
        verify=False,
    )
    # 尝试保存，失败则返回错误信息，成功则返回下载地址
    try:
        path = config.download_path
        with open(path+f'{name}{id}.pdf', 'wb') as f:
            f.write(response.content)

            data = {
                'code': 200,
                'message': 'success',
                'name': name + 'pdf',
            }
        return jsonify(data)
    except Exception as e:
        data = {
            'code': 400,
            'message': '保存失败',
            'name': name + 'pdf',
        }
        print('保存失败，原因：' + str(e))
        return jsonify(data)


if __name__ == '__main__':
    app.run()
