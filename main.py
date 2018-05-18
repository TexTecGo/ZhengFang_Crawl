# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""

# -*- coding: utf-8 -*-
"""
Created on 2018/5/18 

@author: susmote
"""
import requests
from bs4 import BeautifulSoup
from PIL import Image
import time

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Referer' : 'http://125.221.35.100/default2.aspx',
    'Host' : '125.221.35.100'
}
url='http://125.221.35.100/default2.aspx'
session=requests.session()
soup=BeautifulSoup(session.get(url,headers=headers).text,'lxml')
__VIEWSTATE=soup.find_all('input',type="hidden")[0]['value']
number=input('输入账号：')
passwd=input('输入密码：')
t = str(int(time.time()*1000))
captcha_url='http://125.221.35.100/CheckCode.aspx'
r=session.get(captcha_url,headers=headers)
print(r)
with open('captcha.jpg','wb') as f:
    f.write(r.content)
im=Image.open('captcha.jpg')
im.show()
im.close()
checkcode = input("请输入验证码 ： ")

postdata={
    "__VIEWSTATE" : __VIEWSTATE,
    "TextBox1": number,
    "TextBox2": passwd,
    "TextBox3": checkcode,
    "Button1": "",
    'RadioButtonList1': '\xd1\xa7\xc9\xfa',
    'Button1': '',
}

print(postdata)
res=session.post('http://125.221.35.100/default2.aspx',data=postdata,headers=headers)

#
print(res.text)
r = session.get('http://125.221.35.100/xs_main.aspx?xh=2017030548',headers=headers) #如果模拟登录成功，这里返回的是你教务系统的主页源代码
classContent = session.get('http://125.221.35.100/xskbcx.aspx?xh=2017030548&xm=李斯特&gnmkdm=N121603',headers=headers)




print(r.text)
print('学生课表',classContent.text)

UserinfoContent = session.get('http://125.221.35.100/xsgrxx.aspx?xh=2017030548&xm=李斯特&gnmkdm=N121501',headers=headers)
print('学生个人信息',UserinfoContent.text)