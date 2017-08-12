# -*- coding: utf-8 -*-
from selenium import webdriver
from course_parser import Parser
import sys


class SCU(object):
    def __init__(self):
        # 这编码...很烦
        self.account = raw_input('请输入教务处账号:'.decode('utf-8').encode('gbk'))
        self.password = raw_input('请输入教务处密码:'.decode('utf-8').encode('gbk'))
        print u'正在登录...'
        self.browser = webdriver.Chrome()
        self.has_logined = False

    def login(self, url):
        try:
            self.browser.get(url)
            account_elem = self.browser.find_element_by_name("zjh")
            password_elem = self.browser.find_element_by_name("mm")
            account_elem.send_keys(self.account)
            password_elem.send_keys(self.password)
            self.browser.find_element_by_id("btnSure").click()
            print u'登录成功!'
            self.has_logined = True
            return
        except:
            pass

    def get_score_page(self):
        if self.has_logined:
            try:
                self.browser.get('http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3136')
                return self.browser.page_source
            except:
                print u'获取成绩页面失败'
                return
        else:
            print u'你还没有登录!'
            self.login()

    def query_GAP(self):
        page = self.get_score_page()
        parser = Parser(page)
        parser.output()

if __name__ == '__main__':
    SCU_spider = SCU()
    SCU_spider.login('http://zhjw.scu.edu.cn/login.jsp')
    SCU_spider.query_GAP()




