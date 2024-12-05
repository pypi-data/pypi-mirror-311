#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/23 19:36
fileName    : add_ui.py
'''
#  UI
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter import *
from tkinter.ttk import *

# 工具
import os
from urllib.parse import urlparse
from api_project.common.LOG import Logger
from api_project.common.ENV import ENV
from api_project.common.CSV import Writer
from api_project import CASE_CONFIG_PATH, CASE_SCRIPT_DIR_PATH, CASE_DATA_DIR_PATH, FEED, CONFIG_DIR_PATH
from saf.templates.API_Project.api_project import TAB_SPACE
from saf.utils.Curl2Object import Curl, Template


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.file_path = StringVar()
        self.file_path.set('请选择...')
        self.tk_input_file_path = self.__tk_input_file_path(self)
        self.tk_button_choose_file_button = self.__tk_button_choose_file_button(self)
        self.tk_button_start_button = self.__tk_button_start_button(self)
        self.tk_text_log = self.__tk_text_log(self)

    def __win(self):
        self.title("cURL2PyCode v0.1")
        # 设置窗口大小、居中
        width = 400
        height = 200
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)

        self.minsize(width=width, height=height)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)

        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_input_file_path(self, parent):
        ipt = Entry(parent, textvariable=self.file_path)
        ipt.place(relx=0.0000, rely=0.0500, relwidth=0.7500, relheight=0.1500)
        return ipt

    def __tk_button_choose_file_button(self, parent):
        btn = Button(parent, text="选择文件...", takefocus=False, )
        btn.place(relx=0.8000, rely=0.0500, relwidth=0.2000, relheight=0.1500)
        return btn

    def __tk_button_start_button(self, parent):
        btn = Button(parent, text="开 始 转", takefocus=False)
        btn.place(relx=0.2000, rely=0.2800, relwidth=0.5975, relheight=0.1500)
        return btn

    def __tk_text_log(self, parent):
        text = Text(parent)
        text.place(relx=0.0000, rely=0.5000, relwidth=1.0000, relheight=0.5000)
        self.create_bar(parent, text, True, True, 0, 100, 400, 100, 400, 200)
        return text

class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self, Logger())

    def __event_bind(self):
        self.tk_button_choose_file_button.bind('<Button-1>', self.ctl.choose_file)
        self.tk_button_start_button.bind('<Button-1>', self.ctl.run_convert)
        self.tk_text_log.bind('<Delete>', self.ctl.clear_log)
        pass

    def __style_config(self):
        pass

class Controller:
    ui: Win
    logger: Logger
    def __init__(self):
        pass

    def init(self, ui, logger):
        """
        得到UI实例，对组件进行初始化配置
        """
        self.ui = ui
        self.logger = logger
        # TODO 组件初始化 赋值操作
    def choose_file(self,evt):
        self.file_path = askopenfilename(initialdir='~/Desktop',
                                         title='打开cURL命令文件',
                                         filetypes=[('All Files', '*.*')])
        if self.file_path:
            self.ui.file_path.set(self.file_path)
            self.ui.tk_text_log.insert('end', self.logger.info(f"您选择的文件是：{self.file_path}"))
        else:
            self.ui.tk_text_log.insert('end', self.logger.info(f"您取消的选择"))
    def run_convert(self,evt):
        ENV.load()
        result = askstring('提示:', '请输入所有接口路径的前缀:\n例如: https://test.xiaobaiots.com/api/v1')
        if not result:
            self.ui.tk_text_log.insert('end', self.logger.info('您已经取消转换！'))
            return
        else:
            # 重写host_config.py
            code = f'{FEED}'.join([
                "#! /usr/bin/env python",
                "'''",
                "Auther      : xiaobaiTser",
                "Email       : 807447312@qq.com",
                "createTime  : 2024/11/21 19:24",
                "fileName    : host_config.py",
                "'''",
                "",
                "class HOST(object):",
                f"{TAB_SPACE}TEST_HOST: str = '{result}'",
                f"{TAB_SPACE}PRO_HOST: str = '{result}'",
                f"{TAB_SPACE}CURRENT_HOST: str = TEST_HOST",
            ])
            with open(os.path.join(CONFIG_DIR_PATH, 'host_config.py'), 'w', encoding='utf-8') as f:
                f.write(code)
                f.close()
            self.ui.tk_text_log.insert('end', self.logger.info('已经重写host_config.py'))
            os.environ['HOST'] = result

        if self.file_path:
            self.ui.tk_text_log.insert('end', self.logger.info('已经加载环境变量'))
            curl = Curl()
            curl.load(curl_file_path=self.file_path)
            self.ui.tk_text_log.insert('end',
                                       self.logger.info(f'已加载文件[{os.path.split(self.file_path)[1]}]，正在进行转换'))
            for request in curl.group:
                # 获取接口名称：
                if 'API_COUNT' not in os.environ.keys():
                    os.environ['API_COUNT'] = str(0)
                else:
                    os.environ['API_COUNT'] = str(int(os.environ.get('API_COUNT')) + 1)
                _API_NAME_ = urlparse(request.get('url')).path.split('/')[-1]
                API_NAME = _API_NAME_.upper() if _API_NAME_ != '' else f"API_{os.environ.get('API_COUNT')}"
                newline = f"{API_NAME}_CASE_DATA_PATH = os.path.join(CASE_DATA_DIR_PATH, '{API_NAME}.csv'){FEED}"
                try:
                    with open(CASE_CONFIG_PATH, 'r', encoding='utf-8') as fr:
                        alllines = fr.readlines()
                        if newline not in alllines:
                            # 写入测试用例数据路径
                            with open(CASE_CONFIG_PATH, 'a', encoding='utf-8') as fa:
                                fa.write(f"{newline}")
                                fa.close()
                            self.ui.tk_text_log.insert(
                                'end',
                                self.logger.info(f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}成功！")
                            )
                        del alllines
                        fr.close()
                except Exception as e:
                    self.ui.tk_text_log.insert(
                        'end',
                        self.logger.info(f"{os.path.split(CASE_CONFIG_PATH)[1]} 写入{newline}失败：{e}")
                    )

                # 写入测试用例脚本
                CASE_SCRIPT = os.path.join(CASE_SCRIPT_DIR_PATH, f"test_{API_NAME.lower()}.py")
                try:
                    with open(CASE_SCRIPT, 'w', encoding='utf-8') as fw:
                        fw.write(Template.requests_pytest_allure_template(request=request))
                        fw.close()
                    self.ui.tk_text_log.insert(
                        'end',
                        self.logger.info(f"test_{API_NAME.lower()}.py 写入成功！")
                    )
                except Exception as e:
                    self.ui.tk_text_log.insert(
                        'end',
                        self.logger.info(f"test_{API_NAME.lower()}.py 写入失败：{e}")
                    )

                # 写入测试用例数据文件
                CASE_DATA = os.path.join(CASE_DATA_DIR_PATH, f"{API_NAME}.csv")
                if not os.path.isdir(CASE_DATA_DIR_PATH):
                    os.mkdir(CASE_DATA_DIR_PATH)
                try:
                    Writer(file_path=CASE_DATA,
                           data=[list(request.keys()), list(request.values())],
                           ignore_first_row=False)
                    self.ui.tk_text_log.insert(
                        'end',
                        self.logger.info(f"{API_NAME}.csv 写入成功！")
                    )
                except Exception as e:
                    self.ui.tk_text_log.insert(
                        'end',
                        self.logger.error(f"{API_NAME}.csv 写入失败：{e}")
                    )
        else: self.ui.tk_text_log.insert('end', self.logger.error('还未选择需要转换的文件'))

    def clear_log(self,evt):
        self.ui.tk_text_log.delete('1.0', END)

if __name__ == "__main__":
    win = Win(Controller())
    win.mainloop()