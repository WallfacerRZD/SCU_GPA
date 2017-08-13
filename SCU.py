# -*- coding: utf-8 -*-
from selenium import webdriver
from course_parser import Parser
import cookielib
import urllib2
import urllib
import sys


class SCU(object):
    def __init__(self):
        self.url = 'http://zhjw.scu.edu.cn/login.jsp'
        self.login_by_post_url = 'http://zhjw.scu.edu.cn/loginAction.do'
        self.grade_url = 'http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3136'
        print u'请输入教务处账号:'
        self.account = raw_input()
        print u'请输入教务处密码:'
        self.password = raw_input()
        print u'正在登录...'
        self.has_logined = False

    #使用selenium获取成绩页面
    def login_by_selenium(self):
        try:
            self.browser = webdriver.Chrome()
            self.browser.set_window_position(-2000, 0)
            self.browser.get(self.url)
            account_elem = self.browser.find_element_by_name("zjh")
            password_elem = self.browser.find_element_by_name("mm")
            account_elem.send_keys(self.account)
            password_elem.send_keys(self.password)
            self.browser.find_element_by_id("btnSure").click()
            print u'登录成功!'
            return
        except:
            pass

    def get_score_page(self):
        try:
            self.browser.get(self.grade_url)
            page = self.browser.page_source
            print type(page)
            self.browser.quit()
            return page
        except:
            print u'获取成绩页面失败'
            return None

    # 使用cookie登录,获取成绩页面

    def get_login_cookie(self):
        cookie = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        data = urllib.urlencode({
            'zjh': self.account,
            'mm': self.password
        })
        request = urllib2.Request(self.login_by_post_url, data)
        response = opener.open(request)
        if response.code == 200:
            print u'登录成功'
            return cookie
        else:
            print u'登录失败'
            return

    def get_score_page_by_cookie(self):
        try:
            cookie = self.get_login_cookie()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
            request = urllib2.Request(self.grade_url)
            response = opener.open(request)
            page = response.read().decode('gb2312').encode('utf-8')
            return page
        except:
            print u'获取成绩页面失败'
            return None

    def query_GPA(self):
        page = self.get_score_page_by_cookie()
        with open('test.html', 'w') as f:
            f.write(page)
        if page is not None:
            parser = Parser(page)
            parser.output()
        else:
            print u'解析失败'
            return

if __name__ == '__main__':
    SCU_spider = SCU()
    SCU_spider.query_GPA()







