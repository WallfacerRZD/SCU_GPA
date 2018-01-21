# coding:utf-8
from bs4 import BeautifulSoup


# 格式化输出,解决Unicode字符站2个ascii字符宽度

def format_print(my_str, width=40, end=''):
    real_width = 0
    for i in my_str:
        if ord(i) > 127:
            real_width += 2
        else:
            real_width += 1
    print(my_str + ' ' * (width - real_width), end=end)


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
        format_print(self.reason, 10, '\n')


class Parser(object):
    def __init__(self, page):
        self.soup = BeautifulSoup(page, 'html.parser')
        print('正在解析成绩....')

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
        # [课程名, 学分, 课程属性, 成绩, 未通过原因]
        titles = [titles[2], titles[4], titles[5], titles[6], titles[7]]
        return titles

    def get_course_datas(self, table_node):
        def parse_data(data_node):
            child_node = data_node.contents
            if len(child_node) == 1:
                return child_node[0].strip()
            else:
                return child_node[1].string.strip()

        course_nodes = table_node.find_all('tr')
        del course_nodes[0]
        courses = []
        for course_node in course_nodes:
            # 解析数据
            datas = list(map(parse_data, course_node.find_all('td')))
            course = Course(datas[2], datas[4], datas[5], datas[6], datas[7])
            courses.append(course)
        return courses

    def output_titles(self, table_titles):
        for i in range(len(table_titles)):
            if i == 0:
                format_print(table_titles[i], 40)
            else:
                format_print(table_titles[i], 10)
        print()

    def get_grade_piont(self, grade):
        if grade >= 90:
            return 4.0
        if grade >= 85:
            return 3.7
        if grade >= 80:
            return 3.3
        if grade >= 76:
            return 3
        if grade >= 73:
            return 2.7
        if grade >= 70:
            return 2.3
        if grade >= 66:
            return 2
        if grade >= 63:
            return 1.7
        if grade >= 61:
            return 1.3
        if grade >= 60:
            return 1
        if grade < 60:
            return 0

    def get_GPA(self, _credits, scores):
        total_credits = 0
        # 绩点*学分的和
        product_sum = 0
        for i in range(len(_credits)):
            total_credits += _credits[i]
            product_sum += self.get_grade_piont(scores[i]) * _credits[i]

        return product_sum / total_credits

    def get_average(self, credits, scores):
        total_credits = 0
        # 学分*分数的和
        product_sum = 0
        for i in range(len(credits)):
            total_credits += credits[i]
            product_sum += credits[i] * scores[i]
        return product_sum / total_credits

    def output_courses_info(self, courses):
        for course in courses:
            course.show()
        # GPA,average
        _credits = list(map(lambda x: float(x.credit), courses))
        scores = list(map(lambda x: float(x.score), courses))
        GPA = self.get_GPA(_credits, scores)
        average = self.get_average(_credits, scores)
        print('..................................................................................')
        print('GPA:', GPA)
        print('平均分:', average)

    def output(self):
        title = self.get_title()
        table_node = self.get_table_node()
        table_titles = self.get_table_head(table_node)
        courses = self.get_course_datas(table_node)
        print('..................................................................................')
        print(title)
        self.output_titles(table_titles)
        self.output_courses_info(courses)
