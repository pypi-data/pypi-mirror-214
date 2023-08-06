# -*- coding: utf-8 -*-
import sys #내장모듈
import subprocess #내장모듈
import os #내장모듈

import pcell, scolor, mygrid, basic_data, jfinder # my 모듈

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class Main(QMainWindow):
    """
    jfinder를 쉽게 이해하게 하기위해 만든것
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.excel = pcell.pcell()
        self.color = scolor.scolor()
        self.jf = jfinder.jfinder()
        self.basic_d = basic_data.basic_data()
        #self.common_data = self.basic_d.basic_data()
        self.new_menu = []
        self.btn_name_list = []
        self.window_size_x =1000
        self.window_size_y =1000
        self.last_click_menu = ""
        self.last_action_by = "start"


        self.var = {"main_path": "./bori_files", "window_size_x": self.window_size_x, "window_size_y": self.window_size_y, }
        self.menu = {}

        self.basic_width_big = int(self.var["window_size_x"] / 3)
        self.basic_width_small = int(self.var["window_size_x"] / 6)

        self.var['page1_table1_start'] = 0
        self.var['page1_table2_start'] = 0
        self.var['page1_table3_start'] = 0
        self.var['page1_table4_start'] = 0
        self.var['page1_table5_start'] = 0
        self.var['page1_table6_start'] = 0

        self.text_1_list = []
        self.text_2_list = []
        self.text_3_list = []
        self.text_4_list = []
        self.text_5_list = []
        self.text_6_list = []

        self.resize(self.var["window_size_x"], self.var["window_size_y"])
        # 항상위에 떠있게 하는것
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('photo/halmoney_logo.jpg'))
        self.setWindowTitle("Mr.J_Finder / 정규표현식을 좀더 편하게 사용하도록 만든것")

        #self.make_menu_dic()
        self.create_menubar()

        #탭페이지를 3개 만드는것
        tabs = QTabWidget()
        tabs.addTab(self.tab_page_1(), '기본코드')
        tabs.addTab(self.tab_page_2(), '내가 만든 코드')
        self.setCentralWidget(tabs)
        self.show()

        self.page1_menu_list()
        self.make_grid_button_page1_menu_list()

    def check_user_folder(self):
        # user_code라는  folder가 있는지 확인, 없으면 새로 만든다
        path = "pceller/user_code"
        os.makedirs(path, exist_ok=True)

    def check_volunteer_folder(self):
        # volunteer_code라는 folder가 있는지 확인, 없으면 새로 만든다
        path = "pceller/volunteer_code"
        os.makedirs(path, exist_ok=True)

    def page1_menu_list(self):
        #모든 메뉴를 설정한다
        #이것은 입력으로 메뉴종목을 나타낼때 설정하며, var변수에 넣는다
        self.var["text_no"] ={}

        temp_dic_1 = {"최소탐색": [1, '(최소찾기)', "설명 - 1"],
                      "최대탐색": [1, "(최대찾기)", "설명 - 2"],
                      "대소문자무시": [1, "(대소문자무시)", "설명 - 3"],
                      "개행문자포함": [1, "(개행문자포함)", "설명 - 4"],
                      "여러줄로표현": [1, "(여러줄로표현)", "설명 - 5"],
                      }

        #temp_dic_2 = {"맨앞1개만 찾기":[2,""], "찾아서 삭제":[2,""], "찾은것들 리스트로":[2,""], "찾은 위치포함 리스트로":[2,""],"바꾸기":[2,""],}
        temp_dic_2 = { "처음부터 맞아야함":[2,'[처음]', "type_20"],

                       "숫자":[2,"숫자&", "숫자를 검색하는데 사용합니다"],
                       "한글":[2,'한글&', "type_21"],
                       "한글모음":[2,'한글모음&', "한글모음만 솎아내는 것입니다"],
                       "한글자음":[2, '한글자음&', "type_21"],
                       "영어":[2,"영어&", "type_21"],
                       "한자":[2,"한자&", "type_21"],
                       "일어":[2,"일어&", "일본어 글자를 추출하는 것입니다"],

                       "공백(공백, 탭 등)":[2,"공백&", "공백과 탭을 추출하는 것입니다"],
                       "not(포함하지 않음)":[2,"^", "어떤 글자나 문자는 포함하지 않게 하기 위한 것"],
                       "제외": [2, "^", "type_22"],

                       "글자나 문자한개":[2,"[한글자]", "여러갯수가 아니고 한개의 문자만 추출"],

                       "특정단어":[2,"[(특정단어)", "type_24"],
                       "메타문자":[2,"[\메타문자", "type_24"],
                       "특수문자": [2, '[특수문자', "type_24"],
                       "특정단어제외": [2, '[^(제외할단어)', "type_24"],

                       "또는": [2, '|', "type_25"],

                       "다지우기":[2,"(다지우기)", "type_99"],
                       "맨끝까지 맞아야함": [2, '[맨끝]', "정규표현식의 문자가 중간이 아니라 끝까지 다 적용이 되야 할때"],

                       "예)2~5까지의 숫자": [2, "[2-5", "type_24"],
                       "예)c~e까지의 문자": [2, "[c-e", "type_24"],
                       "예)j또는f또는i가 들어간 문자": [2, "[jfi", "type_24"],
                       "예)abc가 들어간 문자": [2, "[(abc)", "type_24"],

                       }
        temp_dic_3 = {"1개":[3,":1~1]", "type_x0"],
                      "1개이상":[3,":1~]", "type_x0"],
                      "1~10개사이":[3,":1~10]", "type_x0"],
                      "0개이상":[3,":0~]", "type_x0"],
                      "0개또는1개":[3,":0~1]", "type_x0"],
                      "n개~m개":[3,":n~m]", "type_x0"],
                      }
        temp_dic_4 = {"abc중 c만 1번이상 반복":[4,"abc[1~]", "type_z0"],
                      "abc중 bc만 1번이상 반복":[4,"a(bc)[1~]", "type_z0"],
                      "a와 b와 c를 제외한 모든 문자": [4, "[^abc]", "type_z0"],
                      "한글로 3~5개의 글자로 된것을 그룹명 짖기": [4, "(?P<그룹명>[한글:3~5])", "type_z0"],
                      "a와 b사이의 모든문자 찾기": [4, "a[문자:1~]b", "type_z0"],
                      "a또는b또는c": [4, "a[또는]b[또는]c", "type_z0"],
                      "전방탐색 : .+(?=:) => :앞의 모든 문자": [4, ".+(?=:)", "type_z0"],
                      "후방탐색 : (?<=\$)[0-9.]+ => $뒤의 숫자": [4, "(?<=\$)[0-9.]+", "type_z0"],
                      "Html태그중 <H숫자>~~<\H숫자>안의 글자": [4, "<H(0-30])>.*?</H\\1>", "type_z0"],
                      "문장중 핸드폰번호 찾기": [4, "0[1~1][숫자:2~2]-[0~1][숫자:3~4]-[0~1][숫자:4~4]", "type_z0"],
                      "2022-01-01형식의 날짜찾기": [4, "[0-9]{4})-([0-9]{2})-([0-9]{2}", "type_z0"],
                      "이메일찾기": [4, "[\w\.-]+@[\w\.-]+", "type_z0"],
                      "괄호안의 숫자 찾기": [4, "([모든문자:0~])", "type_z0"],
                      "지역 전화번호 찾기": [4, "0(2|31|32|33|41|42|43|44|51|52|53|54|55|61|62|63|64)\-{0,1}\d{3,4}\-{0,1}\d{4}", "type_z0"],
                      "주민등록번호": [4, "[0-9]{2}0[1-9]|1[0-2]0[1-9]|[1,2][0-9]|3[0,1]-[1-4][0-9]{6}", "type_z0"],
                      "금액": [4, "[숫자,][1~][원:0~1]", "type_z0"],
                      "중복된 단어 찾기": [4, "\\b(\\w+)\\s+\\1\\b", "type_z0"],
                      }

        self.var["menu_a1"] = list(temp_dic_1.keys())
        self.var["menu_a2"] = list(temp_dic_2.keys())
        self.var["menu_a3"] = list(temp_dic_3.keys())
        self.var["menu_a4"] = list(temp_dic_4.keys())

        self.var["text_no"].update(temp_dic_1)
        self.var["text_no"].update(temp_dic_2)
        self.var["text_no"].update(temp_dic_3)
        self.var["text_no"].update(temp_dic_4)

    def create_menubar(self):
        # 메뉴바를 만드는 것
        menubar = self.menuBar()
        menu_1 = menubar.addMenu("사용법")

        menu_1_1 = QAction('내부실행용', self)
        menu_1_1.triggered.connect(self.show_manual_1)
        menu_1.addAction(menu_1_1)

        menu_1_2 = QAction('외부화일 실행용', self)
        menu_1_2.triggered.connect(self.show_manual_1)
        menu_1.addAction(menu_1_2)

        menu_1_3 = QAction(QIcon("save.png"), '참고사이트', self)
        menu_1_3.triggered.connect(self.show_manual_1)
        menu_1.addAction(menu_1_3)

        menu_2 = menubar.addMenu("Made by")

        menu_2_1 = QAction('누가 만들었나요?', self)
        menu_2_1.triggered.connect(self.show_manual_1)
        menu_2.addAction(menu_2_1)

        menu_2_2 = QAction('Logo의 의미', self)
        menu_2_2.triggered.connect(self.show_manual_1)
        menu_2.addAction(menu_2_2)

        menu_3 = menubar.addMenu("끝내기")

        menu_3_1 = QAction(QIcon('exit.png'), 'Exit', self)
        menu_3_1.triggered.connect(qApp.quit)
        menu_3.addAction(menu_3_1)

    def read_current_path(self):
        """
		현재의 경로를 돌려주는것
		"""
        result = os.getcwd()
        return result

    def read_all_filename_in_folder(self, directory=""):
        """
		폴더안의 모든 화일이름을 읽오오는것
		단, 폴더안의 폴더이름은 제외시킨다
		"""
        if directory == "":
            directory = self.read_current_path()
        result = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return result

    def tab_page_1(self):
        """첫번째 페이지를 만드는 것"""
        Main.keyPressEvent = self.keyPressEvent

        self.page1_table1 = mygrid.CreateTable(30,30)
        self.page1_table1.setColumnWidth(0, 160)
        self.page1_table1.verticalHeader().setVisible(False) #윗부분과 왼쪽의 header를 안보이게 하는것
        self.page1_table1.setHorizontalHeaderLabels(["전체설정"]) #헤더의 이름을 지정
        self.page1_table1.verticalScrollBar().setStyleSheet(("QScrollBar {width:0px;}")) #스크롤바를 안보이게 하는기능은 없어, 넒이를 0으로 만듦

        self.page1_table2 = mygrid.CreateTable(30,30)
        self.page1_table2.setColumnWidth(0, 250)
        self.page1_table2.verticalHeader().setVisible(False)
        self.page1_table2.setHorizontalHeaderLabels(["문자규칙"])
        self.page1_table2.verticalScrollBar().setStyleSheet(("QScrollBar {width:0px;}"))

        self.page1_table3 = mygrid.CreateTable(30,30)
        self.page1_table3.setColumnWidth(0, 160)
        self.page1_table3.verticalHeader().setVisible(False)
        self.page1_table3.setHorizontalHeaderLabels(["갯수설정"])
        self.page1_table3.verticalScrollBar().setStyleSheet(("QScrollBar {width:0px;}"))

        self.page1_table4 = mygrid.CreateTable(30,30)
        self.page1_table4.setColumnWidth(0, 400)
        self.page1_table4.verticalHeader().setVisible(False)
        self.page1_table4.setHorizontalHeaderLabels(["주요샘플"])
        self.page1_table4.verticalScrollBar().setStyleSheet(("QScrollBar {width:0px;}"))

        # 메뉴의 키를 기준으로 리스트형태로 만들어서 버튼메뉴를 만든다
        page1_menu1_list = list(self.menu.keys())
        page1_menu1_list.sort()

        # 각 메소드의 입력값을 넣을수 있는 버튼과 텍스트를 만들기위한 레이아웃이다
        layout_top_3 = QVBoxLayout()
        layout_top_4 = QVBoxLayout()

        #오른쪽 부분에 버튼과 텍스트묶음 형태의 11개의 자료를 만드는 것
        for one in range(1, 12):
            exec("self.btn_c_{} = QPushButton('')".format(one))
            exec("self.btn_c_{}.setMaximumHeight(50)".format(one))
            self.btn_name_list.append("btn_c_{}".format(one))
            exec("layout_top_3.addWidget(self.btn_c_{})".format(one))
            exec("self.text_d_{} = QTextEdit('')".format(one))
            exec("self.text_d_{}.setMaximumHeight(50)".format(one))
            exec("layout_top_4.addWidget(self.text_d_{})".format(one))

        # 메소드의 설명이 나타나는 텍스트영역을 만드는것
        self.page1_main_txt_1 = QPlainTextEdit()
        self.page1_main_txt_1.setFont(QFont('Malgun Gothic', 10))

        self.page1_main_txt_2 = QPlainTextEdit()
        self.page1_main_txt_2.setFont(QFont('Malgun Gothic', 10))
        self.page1_main_txt_2.textChanged.connect(self.event_text_changed_page1_main_txt_2) #Jfinder스타일이 정규표현식으로 바꾸는 것
        self.page1_main_txt_2.selectionChanged.connect(self.event_focus_in_page1_main_txt_2)

        self.page1_main_txt_3 = QPlainTextEdit()
        self.page1_main_txt_3.setFont(QFont('Malgun Gothic', 10))

        # 실행버튼 : 버튼을 누르면 각 메소드가 실행되는 것
        page1_btn_run_1 = QPushButton('전\n체\n설\n정\n(지우기)')
        page1_btn_run_1.setFont(QFont('Malgun Gothic', 10))
        my_rgb_color = self.color.change_scolor_to_rgb("red85")
        my_hex_color = self.color.change_rgb_to_hex(my_rgb_color)
        page1_btn_run_1.setStyleSheet("background-color: {}".format(my_hex_color))
        page1_btn_run_1.clicked.connect(self.action_p1_btn1_run)
        page1_btn_run_1.setSizePolicy(30, QSizePolicy.Preferred)


        page1_btn_run_2 = QPushButton('변\n경\n된\n것\n(지우기)')
        page1_btn_run_2.setFont(QFont('Malgun Gothic', 10))
        page1_btn_run_2.clicked.connect(self.action_p1_btn2_run)
        page1_btn_run_2.setSizePolicy(30, QSizePolicy.Preferred)


        page1_btn_run_3 = QPushButton('정\n규\n식\n(실행)')
        page1_btn_run_3.setFont(QFont('Malgun Gothic', 10))
        page1_btn_run_3.clicked.connect(self.action_p1_btn3_run)
        page1_btn_run_3.setSizePolicy(30, QSizePolicy.Preferred)

        message = """이것을 만든 이유는 정규표현식이 업무에 사용하기 편한것인데
        일반적인 사람들이 읽고 사용하기가 어려워 쉽게 사용할수있도록 만들어 본것이다
        그래서 일부 형식은 기존 정규표현식을 따라간것들도 있다. 단, 너무 복잡한 표현식은 
        """
        self.page1_main_txt_4 = QPlainTextEdit()

        # 위에서 만든 객체들을 각 위치에 넣는다
        layout_right_bottom = QHBoxLayout()

        layout_right_bottom.addLayout(layout_top_3, 2)
        layout_right_bottom.addLayout(layout_top_4, 8)

        layout_left1 = QHBoxLayout()
        layout_left1.addWidget(self.page1_table1, 2)
        layout_left1.addWidget(self.page1_table2, 3)
        layout_left1.addWidget(self.page1_table3, 2)
        layout_left1.addWidget(self.page1_table4, 5)

        layout_right3 = QVBoxLayout()
        layout_right3.addLayout(layout_left1, 5)

        layout_left = QHBoxLayout()
        layout_left.addLayout(layout_right3, 5)

        layout_main = QHBoxLayout()
        layout_main.addWidget(self.page1_main_txt_4, 3)
        layout_main.addWidget(page1_btn_run_1, 1)
        layout_main.addWidget(self.page1_main_txt_1, 3)
        layout_main.addWidget(page1_btn_run_2, 1)
        layout_main.addWidget(self.page1_main_txt_2, 4)
        layout_main.addWidget(page1_btn_run_3, 1)
        layout_main.addWidget(self.page1_main_txt_3, 3)

        layout_right = QVBoxLayout()
        layout_right.addLayout(layout_left, 5)
        layout_right.addLayout(layout_main, 1)

        wdg_1 = QWidget()
        wdg_1.setLayout(layout_right)
        return wdg_1

    def make_grid_button_page1_menu_list(self):
        #앞에서 만든 메뉴들을 그리드안에 버튼으로 만들어 주는 것

        for no in range(len(self.var["menu_a1"])):
            self.page1_table1.write_cell_button([no, 0], self.action_p1_table1_grid_button, self.var["menu_a1"][no])
        for no in range(len(self.var["menu_a2"])):
            self.page1_table2.write_cell_button([no, 0], self.action_p1_table2_grid_button, self.var["menu_a2"][no])
        for no in range(len(self.var["menu_a3"])):
            self.page1_table3.write_cell_button([no, 0], self.action_p1_table3_grid_button, self.var["menu_a3"][no])
        for no in range(len(self.var["menu_a4"])):
            self.page1_table4.write_cell_button([no, 0], self.action_p1_table4_grid_button, self.var["menu_a4"][no])

    def action_p1_table1_grid_button(self):
        #페이지1의 테이블1의 버튼을 누르면 실행되는 코드

        for no in range(len(self.var["menu_a1"])):
            # 맨처음으로 버튼의 모든 속성을 초기화 한다
            self.page1_table1.cellWidget(no, 0).setStyleSheet("background-color: light gray; text-align: left;")

        pushed_button = self.sender() #누른 버튼의 색을 변경한다
        pushed_button.setStyleSheet("background-color: #A1EBFA;font-weight: bold; text-align: left")
        text_value =  self.var["text_no"][pushed_button.text()][1]
        manual = self.var["text_no"][pushed_button.text()][2]
        self.page1_main_txt_4.setPlainText(self.var["text_no"][pushed_button.text()][2])

        main_text = self.page1_main_txt_1.toPlainText()
        self.page1_main_txt_1.setPlainText(main_text +text_value) #기존의 텍스트 내용에 추가된것을 뒤에 넣는것

    def action_p1_table2_grid_button(self):
        self.last_action_by = "button_table2"
        for no in range(len(self.var["menu_a2"])):
            self.page1_table2.cellWidget(no, 0).setStyleSheet("background-color: light gray; text-align: left;")
        pushed_button = self.sender()
        #누른 버튼의 색을 변경한다
        pushed_button.setStyleSheet("background-color: #A1EBFA;font-weight: bold; text-align: left")
        main_text = self.page1_main_txt_2.toPlainText()

        text_value =  self.var["text_no"][pushed_button.text()][1]

        manual = self.var["text_no"][pushed_button.text()][2]
        self.page1_main_txt_4.setPlainText(manual)

        self.now_click_menu = self.var["text_no"][pushed_button.text()][2]
        #기존의 텍스트 내용에 추가된것을 뒤에 넣는것

        #맨처음으로 적용하면 "["를 붙인다
        if self.last_click_menu == "":
            if self.now_click_menu == "type_21": #영어&
                text_value = "[" + text_value
            elif self.now_click_menu == "type_22": #^
                text_value = "[" + text_value
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
        elif self.last_click_menu == "type_20":
            if self.now_click_menu == "type_20": #[맨끝]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_21": #영어&
                text_value = "[" + text_value
            elif self.now_click_menu == "type_22": #^
                text_value = "[" + text_value
            elif self.now_click_menu == "type_23": #[한글자]
                pass
            elif self.now_click_menu == "type_24": #[2-5
                pass
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
        elif self.last_click_menu == "type_21":
            if self.now_click_menu == "type_20": #[맨끝]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_21": #영어&
                text_value = "[" + text_value
            elif self.now_click_menu == "type_22": #^
                text_value = "[" + text_value
            elif self.now_click_menu == "type_23": #[한글자]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_24": #[2-5
                pass
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
        elif self.last_click_menu == "type_22": #^
            if self.now_click_menu == "type_20": #[맨끝]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_21": #영어&
                pass
            elif self.now_click_menu == "type_22": #^
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_23": #[한글자]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_24": #[2-5
                text_value = text_value[1:]
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
            #이것은 잘못된것으로 아무것도 입력하지 않는다
        elif self.last_click_menu == "type_23": #[한글자]
            if self.now_click_menu == "type_20": #[맨끝]
                pass
            elif self.now_click_menu == "type_21": #영어&
                text_value = "[" + text_value
            elif self.now_click_menu == "type_22": #^
                text_value = "[" + text_value
            elif self.now_click_menu == "type_23": #[한글자]
                pass
            elif self.now_click_menu == "type_24": #[2-5
                text_value = "[" + text_value
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
        elif self.last_click_menu == "type_24": #[2-5
            if self.now_click_menu == "type_20": #[맨끝]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_21": #영어&
                pass
            elif self.now_click_menu == "type_22": #^
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_23": #[한글자]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_24": #[2-5
                pass
            elif self.now_click_menu == "type_25": #|
                pass
            else:
                pass
        elif not main_text[-1] in ["&", "]", "^"]:
            if self.now_click_menu == "type_20": #[맨끝]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_21": #영어&
                pass
            elif self.now_click_menu == "type_22": #^
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_23": #[한글자]
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            elif self.now_click_menu == "type_24": #[2-5
                text_value = text_value[1:]
            elif self.now_click_menu == "type_25": #|
                #잘못된거라 값을 넣지 않는다
                text_value = ""
            else:
                pass
        changed_text = str(main_text +text_value)
        changed_text = changed_text.replace("[[", "[")
        self.page1_main_txt_2.setPlainText(changed_text)
        self.last_click_menu = self.var["text_no"][pushed_button.text()]
        self.last_click_menu = self.now_click_menu



    def action_p1_table3_grid_button(self):
        self.last_action_by = "button_table3"
        for no in range(len(self.var["menu_a3"])):
            self.page1_table3.cellWidget(no, 0).setStyleSheet("background-color: light gray; text-align: left")
        pushed_button = self.sender()
        #누른 버튼의 색을 변경한다
        pushed_button.setStyleSheet("background-color: #A1EBFA;font-weight: bold; text-align: left")
        main_text = self.page1_main_txt_2.toPlainText()
        text_value =  self.var["text_no"][pushed_button.text()][1]
        self.now_click_menu = self.var["text_no"][pushed_button.text()][2]
        #기존의 텍스트 내용에 추가된것을 뒤에 넣는것

        print(self.last_click_menu)

        #맨처음으로 적용하면 "["를 붙인다
        if self.last_click_menu == "type_20":
            pass
        elif self.last_click_menu == "type_21":
            main_text = main_text[:-1]
        elif self.last_click_menu == "type_22":
            #이것은 잘못된것으로 아무것도 입력하지 않는다
            text_value = ""
        elif self.last_click_menu == "type_23":
            text_value = "["+text_value
        elif self.last_click_menu == "type_24":
            text_value = text_value[1:]
        elif not main_text[-1] in ["&", "]", "^"]:
            text_value = "[" + text_value[1:]
        elif self.last_click_menu == "":
            text_value = "[" + text_value[1:]
        else :
            pass

        changed_text = str(main_text + text_value)
        changed_text = changed_text.replace("[[", "[")

        self.page1_main_txt_2.setPlainText(changed_text)
        self.last_click_menu = self.now_click_menu[2]

    def action_p1_table4_grid_button(self):
        for no in range(len(self.var["menu_a4"])):
            self.page1_table4.cellWidget(no, 0).setStyleSheet("background-color: light gray; text-align: left;")
        pushed_button = self.sender()
        pushed_button.setStyleSheet("background-color: #A1EBFA;font-weight: bold; text-align: left")
        main_text = self.page1_main_txt_2.toPlainText()
        text_value =  self.var["text_no"][pushed_button.text()][1]

        manual = self.var["text_no"][pushed_button.text()][2]
        self.page1_main_txt_4.setPlainText(manual)

        if main_text[-1] == "&":
            main_text = main_text[:-1]
        if main_text[-1] == "]" :
            main_text = main_text +"["
        self.page1_main_txt_2.setPlainText(main_text +text_value)

    def action_p1_btn1_run(self):
        """버튼을 누르면 pcell의 메소드를 실행 시키는것"""
        self.page1_main_txt_1.setPlainText("")
        self.last_click_menu = ""

    def action_p1_btn2_run(self):
        """버튼을 누르면 pcell의 메소드를 실행 시키는것"""
        self.page1_main_txt_2.setPlainText("")

    def action_p1_btn3_run(self):
        """버튼을 누르면 엑셀의 자료를 찾아서 변경하는것"""
        x1, y1, x2, y2 = self.excel.read_usedrange_address("")
        sql = self.page1_main_txt_3.toPlainText()
        for x in range(x1, x2):
            value = self.excel.read_cell_value("", [x,1])
            result  = self.jf.run_all(sql, value)

    def event_focus_in_page1_main_txt_2(self):
        print(self.page1_main_txt_2.toPlainText())

    def event_text_changed_page1_main_txt_2(self):
        #jfsql이 바뀌면 resql을바꿔서 보여주는것
        new_jsql = self.jf.change_jfsql_to_resql(self.page1_main_txt_2.toPlainText())
        self.page1_main_txt_3.setPlainText(new_jsql)

    def tab_page_2(self):
        Main.keyPressEvent = self.keyPressEvent
        # 두번째 탭은 사용자가 만든 코드를 한번 저장해 놓으면 사용가능하도록 하는 것이다
        user_filesss = self.read_all_filename_in_folder(self.var["main_path"] + "/user_code")
        for one_file in user_filesss:
            if one_file.endswith(".py"):
                self.new_menu.append(one_file)

        # user_code의 갯수를 파악해서 셀의 갯수를 만드는 것이다
        x_no = int(len(self.new_menu) / 2) + 6
        self.page2_table1 = mygrid.CreateTable(x_no, 2)
        self.page2_table1.setColumnWidth(0, 250)
        self.page2_table1.setColumnWidth(1, 250)

        # 기본 메뉴를 테이블에 만든다
        # [버튼위치], [누르면 실행될 코드], [버튼에나타나는 문구]
        for no in range(len(self.new_menu)):
            x, y = divmod(no, 2)
            self.page2_table1.write_cell_button([x, y], self.click_page2_run_button, self.new_menu[no])

        # 메소의 설명이 나타나는 텍스트
        self.page2_main_txt1 = QPlainTextEdit()
        self.page2_main_txt1.setFont(QFont('Malgun Gothic', 11))
        self.page2_main_txt1.setStyleSheet('color:black;font-size:11px;')
        self.page2_main_txt1.setPlainText("이 실행화일이 있는 폴더안의 \nuser_folder안의 파이썬 화일을 실행 시키는 것이다\n입력받으면서 실행될 부분은 별도로 처리하여야 합니다. 단 외부 코드를 실행시키기 위해서는 \n - python 3.8이후 버전설치\n - pywin32설치\n - halmoney모듈의 살치")

        # 실행버튼 : 버튼을 누르면 각 메소드가 실행되는 것
        my_rgb_color = self.color.change_scolor_to_rgb("blu85")
        my_hex_color = self.color.change_rgb_to_hex(my_rgb_color)

        page2_btn_run = QPushButton('실행')
        page2_btn_run.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        page2_btn_run.setStyleSheet("font-weight: bold")
        page2_btn_run.setFont(QFont('Malgun Gothic', 15))
        page2_btn_run.setStyleSheet("background-color: {}".format(my_hex_color))
        page2_btn_run.clicked.connect(self.action_page2_run_button)

        layout_left = QHBoxLayout()
        layout_left.addWidget(self.page2_table1)

        layout_right = QHBoxLayout()
        layout_right.addWidget(self.page2_main_txt1, 5)
        layout_right.addWidget(page2_btn_run, 2)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_left, 5)
        layout_main.addLayout(layout_right, 2)

        wdg_1 = QWidget()
        wdg_1.setLayout(layout_main)
        return wdg_1

    def action_page2_run_button(self):
        file_path = ".\\pceller\\user_code\\" + self.page2_main_txt1.toPlainText()
        print(file_path)
        subprocess.call(["python", file_path])

    def click_page2_run_button(self):
        # page2의 그리드안의 버튼을 누르면 실행되는것
        for no in range(len(self.new_menu)):
            x, y = divmod(no, 2)
            self.page2_table1.cellWidget(x, y).setStyleSheet("background-color: light gray")

        pushed_button = self.sender()
        title = pushed_button.text()
        pushed_button.setStyleSheet("background-color: #A1EBFA")
        self.page2_main_txt1.setPlainText(title)

    def clear_button_text_all(self):
        """ 오른쪽에 만든 11개의 버튼과 텍스트의 글자를 다 지운다 """
        for one in self.btn_name_list:
            exec("self.{}.setText('')".format(one))

        for num in range(1, len(self.btn_name_list) + 1):
            exec("self.text_d_{}.setText('')".format(str(num)))

    def show_manual_1(self):
        # 내부실행용 사용법
        message = """
            메뉴얼1
        """
        self.page1_main_txt_1.setPlainText(message.replace("        ", ""))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont('Malgun Gothic', 8), "QLineEdit")
    app.setFont(QFont('Malgun Gothic', 8), "QPushButton")
    main = Main()
    sys.exit(app.exec_())