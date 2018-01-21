# coding:utf-8
from course_parser import Parser
import requests


class SCU(object):
    def __init__(self):
        self.url = 'http://zhjw.scu.edu.cn/login.jsp'
        self.login_url = 'http://zhjw.scu.edu.cn/loginAction.do'
        self.grade_url = 'http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=fainfo&fajhh=3136'
        self.account = input('请输入教务处账号:')
        self.password = input('请输入教务处密码:')
        print('正在登录...')
        self.has_logined = False

    def login(self):
        s = requests.Session()
        form_data = {
            'zjh': self.account,
            'mm': self.password,
        }
        s.post(self.login_url, data=form_data)
        return s

    def get_score_page(self):
        try:
            s = self.login()
            response = s.get(self.grade_url)
            page = response.text
            return page
        except:
            print('获取成绩页面失败,请检查账号密码')
            return None

    def query_GPA(self):
        page = self.get_score_page()
        if page is not None:
            parser = Parser(page)
            parser.output()
        else:
            print('解析失败')


if __name__ == '__main__':
    SCU_spider = SCU()
    SCU_spider.query_GPA()
