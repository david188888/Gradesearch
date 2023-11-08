import requests
import time
from json import loads,dump
# from os import system

# 1. using requests to get the html


def session_get_html(headers,user):

    data = {
        'account':user['account'],
        'password': user['password']
    }


    pdata = {
    'xnm': user['year'],
    'xqm': user['term'],
    '_search': 'false',
    'nd': 1699411807552,
    'queryModel.showCount': 15,
    'queryModel.currentPage': 1,
    'queryModel.sortName': '',
    'queryModel.sortOrder': 'asc',
    'time': 1
    }


    session = requests.Session()
    session.get('https://sso.scnu.edu.cn/AccountService/openapi/auth.html?client_id=9347e8e342e93da94c8ecf27a9de2599&response_type=code&redirect_url=https://jwxt.scnu.edu.cn/sso/oauthLogin', headers=headers)
    session.post('https://sso.scnu.edu.cn/AccountService/user/login.html', headers=headers, data=data) 
    time.sleep(5)
    cookies = session.cookies
    print(cookies)
    session.get('https://sso.scnu.edu.cn/AccountService/openapi/onekeyapp.html?app_id=96', headers=headers)
    session.get('https://jwxt.scnu.edu.cn/xtgl/login_loginIndex.html', headers=headers)
    get_cookies = session.cookies
    time.sleep(5)
    response = session.post(
        'https://jwxt.scnu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su=20223802048',
        headers=headers,
        data=pdata,
        cookies=get_cookies,
    )
    return response



def deal_score(response,user):
    xnm = user['year']
    xqm = user['term']
    print(str(xnm)+'学年'+str(xnm)+'学期成绩已出 '+str(len(loads(response.text)['items']))+' 门\n')
    title=['课程名称','成绩','绩点','学分','学分绩点']
    print(' | '.join(title))
    for i in loads(response.text)['items']:
        print()
        print(' | '.join([i['kcmc'], i['cj'], i['jd'], i['xf'], i['xfjd']]))



if __name__ == '__main__':
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        with open('./user.json', 'r') as f:
            user = loads(f.read())
            deal_score(session_get_html(headers,user),user)
    
    except:
        print('配置用户信息')
        account = int(input('请输入学号：'))
        password = input('请输入密码：')
        year = int(input('请输入学年：'))
        term = int(input('请输入学期：'))

        if term == 1:
            term = 3
        elif term == 2:
            term = 12
        else:
            print('输入错误')
            exit()

        user = {
            'account':account,
            'password':password,
            'year':year,
            'term':term
        }

        with open ('./user.json','w') as f:
            dump(user,f)

        deal_score(session_get_html(headers,user),user)

    # initial the settings


    # system('pause') # windows -> .exe




