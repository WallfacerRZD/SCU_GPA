# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import time

# 格式化输出,解决Unicode字符站2个ascii字符宽度
def format_print(my_str, width=40):
    real_width = 0
    for i in my_str:
        if ord(i) > 127:
            real_width += 2
        else:
            real_width += 1
    print my_str + ' ' * (width - real_width),


class Course(object):

    def __init__(self, name, credit, attr, score, reason):
        self.name = name
        self.credit = credit
        self.attr = attr
        self.score = score
        self.reason = reason if reason else u'无'

    def show(self):
        format_print(self.name, 40)
        format_print(self.credit, 10)
        format_print(self.attr, 10)
        format_print(self.score, 10)
        format_print(self.reason, 10)
        print


class Parser(object):
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')
        print u'正在解析成绩....'

    def get_title(self):
        return self.soup.find('table', border="0", align="left", cellpadding="0").find('b').string

    def get_table_node(self):
        return self.soup.find('table', class_="displayTag")


    # [课程号, 课序号, 课程名, 英文课程名, 学分, 课程属性, 成绩, 未通过原因]
    def get_table_head(self, table_node):
        titles_node = table_node.find('thead').find_all('th')
        titles = []
        for title in titles_node:
            titles.append(title.string.strip())
        titles = [titles[2], titles[4], titles[5], titles[6], titles[7]]
        return titles


    def get_course_datas(self, table_node):
        def parse_data(data_node):
            child_node = data_node.contents
            if len(child_node) == 1:
                return child_node[0].strip()
            else:
                return child_node[1].string.strip()

        course_nodes = table_node.find('tbody').find_all('tr')
        courses = []
        for course_node in course_nodes:
            # 解析数据
            datas = map(parse_data, course_node.find_all('td'))
            course = Course(datas[2], datas[4], datas[5], datas[6], datas[7])
            courses.append(course)
        return courses

    def output(self):
        title = self.get_title()
        table_node = self.get_table_node()
        table_titles = self.get_table_head(table_node)
        courses = self.get_course_datas(table_node)
        for i in range(len(table_titles)):
            if i == 0:
                format_print(table_titles[i], 40)
            else:
                format_print(table_titles[i], 10)
        print
        for course in courses:
            course.show()

