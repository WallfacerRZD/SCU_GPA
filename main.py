# coding:utf-8
import urllib2
import urllib
import cookielib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()
browser.get('http://zhjw.scu.edu.cn/login.jsp')
assert u'四川大学' in browser.title
# login
account = '2016141462307'
password = '044373'
account_elem = browser.find_element_by_name("zjh")
password_elem = browser.find_element_by_name("mm")
try:
    account_elem.send_keys(account)
    password_elem.send_keys(password)
    browser.find_element_by_id("btnSure").click()
except:
    print '登录失败'
print '登录成功'

# 解析成绩
browser.get('http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3136')
print browser.page_source


