# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""

import requests
from bs4 import BeautifulSoup
from PIL import Image
from get_operate_link import get_operate_link
from crawl_func import get_timetable_dic,get_student_info

if __name__ == "__main__":

    #全局变量
    host = "125.221.35.100"  # 学校教务管理系统ip地址，可以改成你们学校的

    url='http://'+host + "/" + 'default2.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Referer': url,
        'Host': host
    }
    session=requests.session()


    # 获取标识码
    soup=BeautifulSoup(session.get(url,headers=headers).text,'lxml')
    __VIEWSTATE=soup.find_all('input',type="hidden")[0]['value']

    # 输入需要的信息 学号，密码，验证码
    studentid = input('输入学号：')
    passwd = input('输入密码：')
    captcha_url = 'http://'+host + "/" + 'CheckCode.aspx'
    r=session.get(captcha_url,headers=headers)
    print(r)
    with open('captcha.jpg','wb') as f:
        f.write(r.content)
    im=Image.open('captcha.jpg')
    im.show()
    im.close()
    checkcode = input("请输入验证码 ： ")

    # 封装需要post的数据
    postdata={
        "__VIEWSTATE": __VIEWSTATE,
        "TextBox1": studentid,
        "TextBox2": passwd,
        "TextBox3": checkcode,
        "Button1": "",
        'RadioButtonList1': '\xd1\xa7\xc9\xfa',
        'Button1': '',
    }

    res = session.post(url, data=postdata, headers=headers)

    if '验证码不正确' in res.text:
        print("你输入的验证码不正确，请重新登录")
        exit()

    # 登录成功后，返回的是你教务系统的主页源代码
    r = session.get('http://'+host + "/" + 'xs_main.aspx?xh='+ studentid,headers=headers)

    link_dic = get_operate_link(host, r.text)
    print(link_dic)

    # 获取学生个人课表
    student_class = session.get(link_dic['学生个人课表'], headers=headers)
    print(get_student_info(student_class.text))
    print(get_timetable_dic(student_class.text))

    # 查询个人成绩
    student_grade_query = session.get(link_dic['成绩查询'], headers=headers)
    print(student_grade_query.text)
    soup = BeautifulSoup(student_grade_query.text, 'lxml')
    __VIEWSTATE = soup.find_all('input', type="hidden")[0]['value']
    query_post_data = {
        '__VIEWSTATE': __VIEWSTATE,
        'ddlXN':'',
        'ddlXQ': '1',
        'Button1': ''
    }
    headers['Referer'] = link_dic['成绩查询']
    user_grade = session.post(link_dic['成绩查询'], data=query_post_data, headers=headers)
    print('user_grade',user_grade.text)

