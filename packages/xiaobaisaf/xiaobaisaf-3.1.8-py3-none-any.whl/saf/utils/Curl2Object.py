#! /usr/bin/env python
'''
Auther      : xiaobaiTser
Email       : 807447312@qq.com
createTime  : 2024/11/15 22:46
fileName    : Curl2Object.py
'''
import shlex
import os
from datetime import datetime
from re import match
from urllib.parse import urlparse
INDENT = 4
TAB_SPACE = INDENT * ' '
FEED = '\n' if os.name == 'nt' else '\r\n'

class Template(object):
    T1 = 'python_requests'
    T2 = 'python_requests_pytest_allure'

    INIT_HEADER_LIST = [
        '#! /usr/bin/env python',
        '# 描述：本代码有周口小白职业培训学校自动化代码生成工具生成，请勿用于商业用途，如有问题请联系我们',
        '# Auther      : xiaobaiTser',
        '# Email       : 807447312@qq.com',
        f'# createTime  : {datetime.now().strftime("%Y/%m/%d %H:%M")}',
        ''
    ]

    T1_HEADER_LIST = INIT_HEADER_LIST + [
        'try:',
        TAB_SPACE + 'import requests',
        'except Exception as e:',
        TAB_SPACE + 'import os',
        TAB_SPACE + 'os.system(\'pip install requests\')',
        ''
    ]

    T2_HEADER_LIST = T4_HEADER_LIST = INIT_HEADER_LIST + [
        'try:',
        TAB_SPACE + 'import requests',
        'except Exception as e:',
        TAB_SPACE + 'import os',
        TAB_SPACE + 'os.system(\'pip install requests\')',
        'try:',
        TAB_SPACE + 'import pytest',
        'except Exception as e:',
        TAB_SPACE + 'import os',
        TAB_SPACE + 'os.system(\'pip install pytest\')',
        'try:',
        TAB_SPACE + 'import allure',
        'except Exception as e:',
        TAB_SPACE + 'import os',
        TAB_SPACE + 'os.system(\'pip install allure-pytest\')',
        'from ..apis.Client import *',
        'from ..common.CSV import Reader',
    ]

    @classmethod
    def requests_template(cls, request: dict, add_import: bool = False) -> str:
        '''
        通过模板生成python_requests代码
        :param request: {'url': '', 'method': 'GET', 'headers': dict(), 'data': ''}
        :return:
        import requests

        url = 'https://www.xiaobai.com/api/v1/login'
        headers = {'content-type':'application/json'}
        data = '{"username":"xiaobai", "password":"123456"}'
        response = requests.request(method='POST', url=url, headers=headers, data=data)

        assert 200 == response.json()['ErrorCode']
        ...
        '''

        code_line_list = [
            '',
            f"url = '{request.get('url')}'",
            f"headers = {request.get('headers')}",
            f"response = requests.request(method='{request.get('method')}', url=url, headers=headers, data=data, verify=False)",
            '',
            '# 断言，自行完善',
            'assert 200 == response.status_code',
            ''
        ]
        if str(request.get('method')).upper() != 'GET':
            code_line_list.insert(3, f"data = '{request.get('data')}'")
        if add_import:
            code_line_list = cls.T1_HEADER_LIST + code_line_list
        return FEED.join(code_line_list)

    @classmethod
    def requests_pytest_allure_template(cls, request: dict, add_import: bool = True) -> str:
        '''
        通过模板生成python_requests_pytest代码
        :param request: {'url': '', 'method': 'GET', 'headers': dict(), 'data': ''}
        :return:

        import os
        import pytest
        import allure
        from ..apis.Client import *
        from ..common.CSV import Reader
        from ..config.case_config import 接口名称_CASE_DATA_PATH

        # @allure.story('接口名称')
        @pytest.mark.parametrize(','.join(Reader(接口名称_CASE_DATA_PATH, False)[0]), Reader(接口名称_CASE_DATA_PATH, True))
        def test_接口名称(method, uri, headers, data):
            allure.step('接口名称-请求')
            response = APIClient.session(method=method, url=os.environ.get('HOST') + uri, headers=eval(headers), data=data,
                                         auth_username='root', auth_password='r00t@xiaobaiaiservice')

            allure.step('接口名称-断言')
            json_assert(response, expression='code', value=0)

            # allure.step('接口名称-提取器')
            # json_extractor()
            ...
        '''
        if 'API_COUNT' not in os.environ.keys():
            os.environ['API_COUNT'] = str(0)
        else:
            os.environ['API_COUNT'] = str(int(os.environ.get('API_COUNT')) + 1)
        _API_NAME_ = urlparse(request.get('url')).path.split('/')[-1]
        API_NAME = _API_NAME_.upper() if _API_NAME_ != '' else f"API_{os.environ.get('API_COUNT')}"
        API_PARAMS_FOTMATER = ', '.join(request.keys())
        API_REQUEST_FORMATER = ', '.join([f"{key}='{value}'"  for key, value in request.items() if key != 'headers'])
        API_REQUEST_FORMATER = API_REQUEST_FORMATER + f", headers={request['headers']}"

        code_line_list = [
            f'from ..config.case_config import {API_NAME}_CASE_DATA_PATH',
            '',
            f'@allure.story("{API_NAME}")',
            f"@pytest.mark.parametrize('{API_PARAMS_FOTMATER}', Reader({API_NAME}_CASE_DATA_PATH, True))",
            f"def test_{API_NAME.lower()}({API_PARAMS_FOTMATER}):",
            f"{TAB_SPACE}allure.step('{API_NAME} 请求')",
            f"{TAB_SPACE}response = APIClient.session({API_REQUEST_FORMATER})",
            f"{TAB_SPACE}",
            f"{TAB_SPACE}allure.step('{API_NAME}-断言')",
            f"{TAB_SPACE}assert response.status_code == 200"
            f"{TAB_SPACE}# json_assert(response, expression='jsonpath表达式', value=预期值)  # 依据接口文档修改",
            f"{TAB_SPACE}",
            f"{TAB_SPACE}# allure.step('{API_NAME}-提取器')",
            f"{TAB_SPACE}# json_extractor(response, env_name='变量名', expression='jsonpath表达式', index=0, default=默认值)",
            f"{TAB_SPACE}# 调用格式：os.environ.get('变量名')"
            ''
        ]
        if add_import:
            code_line_list = cls.T2_HEADER_LIST + code_line_list
        return FEED.join(code_line_list)

class Curl(object):
    def __init__(self):
        self.group        :list = []

    def str2obj(self, one_curl_str: str = ''):
        _request_: dict = {
            'url': '',
            'method': 'GET',
            'headers': dict(),
            'params': '',
            'data': ''
        }
        one_curl_str = one_curl_str.strip()
        try:
            args = shlex.split(one_curl_str)
            for index, arg in enumerate(args):
                if arg.startswith('-'):
                    if args[index + 1].startswith('^'):
                        args[index + 1] = args[index + 1].replace('^', '')
                    # if args[index + 1].endswith('^'):
                    #     args[index + 1] = args[index + 1][:-1]
                if arg == '-X':
                    _request_['method'] = args[index + 1]
                elif arg in ['-H', '--header']:
                    _request_['headers'][args[index + 1].split(':')[0]] = args[index + 1].split(':')[1].strip()
                elif arg in ['-d', '--data', '--data-ascii', '--data-raw', '--data-binary']:
                    _request_['data'] = args[index + 1]
                    _request_['method'] = 'POST'
                else:
                    r = match(r'^[\^a-zA-Z]+?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f\^]))+$', arg)
                    if r:
                        if arg.startswith('^'):
                            arg = arg[1:]
                        if arg.endswith('^'):
                            arg = arg[:-1]
                        # 分域名、路径、参数
                        _request_['url'] = urlparse(arg).path.replace(urlparse(os.environ['HOST']).path, '')
                        _request_['params'] = urlparse(arg).query
            self.group.append(_request_)
        except Exception as e:
            print(e)
        del _request_

    def obj2framework(self):
        '''
           ----project
          |
          |----apis（接口封装）
          |   |
          |   |----Client.py
          |
          |----case_scripts（用例）
          |   |
          |   |----test_*.py
          |   |----test_*.py
          |
          |----case_data_files（用例数据）
          |   |
          |   |----*_CASE_DATA.csv
          |
          |----common（公共方法）
          |   |
          |   |----csvUtils.py
          |   |----jsonUtils.py
          |   |----yamlUtils.py
          |   |----emailService.py
          |
          |----config（配置数据）
          |   |
          |   |----config.py
          |   |----email_service.py
          |   |----jenkins_service.py
          |
          |----data（测试数据）
          |   |
          |   |----*
          |
          |----report（pytest测试报告）
          |   |
          |   |----（默认为空，执行前清空文件等内容）
          |
          |----allure-report（allure测试报告）
          |   |
          |   |----index.html
          |   |----*
          |
          |----run_main.py
        :return:
        '''

    # @classmethod
    def load(slef, curl_str: str = None, curl_file_path: str = None):
        '''
        加载curl字符串或者文件
        解析curl数据中的url、method、headers、cookies、data
        :param curl_str         :   CURL字符串
        :param curl_file_path   :   CURL文件(文本文件类型)
        :return:

        例如：
        Curl.load(curl_str="curl 'http://www.example.com/' -X 'GET'")
        Curl.load(curl_file_path="~/Desktop/curl_data.txt")
        '''
        if curl_str:
            if curl_str.count('curl ') == 1:
                if '^' in curl_str:
                    curl_str = curl_str.replace('^', '')
                slef.str2obj(curl_str[5:])
            elif curl_str.count('curl ') > 1:
                for curl in curl_str.split('curl ')[1:]:
                    slef.str2obj(curl)
            else:
                pass
        elif curl_file_path and os.path.isfile(curl_file_path):
            with open(curl_file_path, 'r', encoding='utf-8') as f:
                curl_str = f.read()
                f.close()
            slef.load(curl_str)
        else:
            pass

    # @classmethod
    def dump(self, template: Template = Template.T1, project_dir: str = ''):
        '''
        将curl数据转换成Python_requests\对象
        :param target:
        :param curl_file_path:
        :return:
        '''
        # SCRIPT_DIR = os.path.join(project_dir, 'case_scripts')

# if __name__ == '__main__':
#     from dotenv import load_dotenv
#     load_dotenv()
#     os.environ['HOST'] = 'https://gitee.com'
#     s = 'C:\\Users\\Administrator\\Desktop\\GET.bat'
#     c = Curl()
#     c.load(curl_file_path=s)
#     # print(len(c.group),c.group)
#     for request in c.group:
#         print(Template.requests_pytest_allure_template(request=request))
