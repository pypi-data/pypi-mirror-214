import json
import time
import os
from json import loads as json_loads
from os import path as os_path, getenv
from sys import exit as sys_exit
from getpass import getpass
import re
import base64
import io

from requests import session, post, adapters

adapters.DEFAULT_RETRIES = 5


class Fudan:
    """
    建立与复旦服务器的会话，执行登录/登出操作
    """

    UA = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0"
    )

    # 初始化会话
    def __init__(
        self,
        uid,
        psw,
        url_login='https://uis.fudan.edu.cn/authserver/login',
        url_code="https://zlapp.fudan.edu.cn/backend/default/code",
        verbose: bool = True,
    ):
        """
        初始化一个session，及登录信息
        :param uid: 学号
        :param psw: 密码
        :param url_login: 登录页，默认服务为空
        """
        self.session = session()
        self.session.keep_alive = False  # type: ignore
        self.session.headers['User-Agent'] = self.UA
        self.url_login = url_login
        self.url_code = url_code

        self.uid = uid
        self.psw = psw
        self.verbose = verbose

    def _page_init(self):
        """
        检查是否能打开登录页面
        :return: 登录页page source
        """
        if self.verbose:
            print("Initiating——", end='')
        page_login = self.session.get(self.url_login)

        if self.verbose:
            print("return status code", page_login.status_code)

        if page_login.status_code == 200:
            if self.verbose:
                print("Initiated——", end="")
            return page_login.text
        else:
            if self.verbose:
                print("Fail to open Login Page, Check your Internet connection\n")
            self.close()
            raise ConnectionError

    def login(self):
        """
        执行登录
        """
        page_login = self._page_init()

        if self.verbose:
            print("getting tokens")
        data = {
            "username": self.uid,
            "password": self.psw,
            "service": "https://zlapp.fudan.edu.cn/site/ncov/fudanDaily",
        }

        # 获取登录页上的令牌
        result = re.findall(
            r'<input type="hidden" name="([a-zA-Z0-9\-_]+)" value="([a-zA-Z0-9\-_]+)"/?>',
            page_login,
        )
        # print(result)
        # result 是一个列表，列表中的每一项是包含 name 和 value 的 tuple，例如
        # [('lt', 'LT-6711210-Ia3WttcMvLBWNBygRNHdNzHzB49jlQ1602983174755-7xmC-cas'), ('dllt', 'userNamePasswordLogin'), ('execution', 'e1s1'), ('_eventId', 'submit'), ('rmShown', '1')]
        data.update(result)

        headers = {
            "Host": "uis.fudan.edu.cn",
            "Origin": "https://uis.fudan.edu.cn",
            "Referer": self.url_login,
            "User-Agent": self.UA,
        }

        if self.verbose:
            print("Login ing——", end="")
        post = self.session.post(
            self.url_login, data=data, headers=headers, allow_redirects=False
        )

        if self.verbose:
            print("return status code", post.status_code)

        if post.status_code == 302:
            if self.verbose:
                print(
                    "\n***********************" "\n登录成功" "\n***********************\n"
                )
        else:
            if self.verbose:
                print("登录失败，请检查账号信息")
            self.close()

    def logout(self):
        """
        执行登出
        """
        exit_url = (
            'https://uis.fudan.edu.cn/authserver/logout?service=/authserver/login'
        )
        expire = self.session.get(exit_url).headers.get('Set-Cookie')
        assert expire is not None
        # print(expire)

        if self.verbose:
            if '01-Jan-1970' in expire:
                print("登出完毕")
            else:
                print("登出异常")

    def close(self, exit_code=0, exit: bool = True):
        """
        执行登出并关闭会话
        """
        self.logout()
        self.session.close()
        if self.verbose:
            print("关闭会话")
            print("************************")
        if exit:
            sys_exit(exit_code)


class FudanJwfw(Fudan):
    def get_grades_html(self) -> str:
        """
        Get the html source of the grades page
        """
        resp = self.session.get(
            'https://jwfw.fudan.edu.cn/eams/teach/grade/course/person!search.action?semesterId=425&projectType=&projectId=1'
        )
        return resp.text

    def parse_grades_html(self, grades_html: str) -> list[dict[str, str]]:
        from bs4 import BeautifulSoup

        def parse_html(html_str):
            soup = BeautifulSoup(html_str, 'html.parser')

            try:
                table = soup.find(
                    'table', {'class': 'gridtable'}
                )  # find the table by its class

                headers = [
                    header.text for header in table.find_all('th')  # type: ignore
                ]  # extract the headers # type: ignore

                records = []

                # iterate over each row in the table
                for row in table.find_all('tr'):  # type: ignore
                    cells = row.find_all('td')

                    # check if there are as many cells as headers (to exclude header row)
                    if len(cells) == len(headers):
                        # construct a dictionary for each row, pairing headers and cell values
                        record = {headers[i]: cell.text for i, cell in enumerate(cells)}
                        records.append(record)
            except:
                print(html_str)
                raise

            return records

        grades = parse_html(grades_html)
        # do .strip() on the values
        return [{k: v.strip() for k, v in g.items()} for g in grades]


def get_account(verbose: bool = True):
    """
    获取账号信息
    """
    uid = getenv("STD_ID") or getenv('FUDAN_PID')
    psw = getenv("PASSWORD") or getenv('FUDAN_PW')
    if uid != None and psw != None:
        if verbose:
            print("从环境变量中获取了用户名和密码！")
        return uid, psw
    print("\n\n请仔细阅读以下日志！！\n请仔细阅读以下日志！！！！\n请仔细阅读以下日志！！！！！！\n\n")
    if os_path.exists("account.txt"):
        print("读取账号中……")
        with open("account.txt", "r") as old:
            raw = old.readlines()
        if (raw[0][:3] != "uid") or (len(raw[0]) < 10):
            print("account.txt 内容无效, 请手动修改内容")
            sys_exit()
        uid = (raw[0].split(":"))[1].strip()
        psw = (raw[1].split(":"))[1].strip()

    else:
        if verbose:
            print("未找到account.txt, 判断为首次运行, 请接下来依次输入学号密码")
        uid = input("学号：")
        psw = getpass("密码：")
        with open("account.txt", "w") as new:
            tmp = (
                "uid:"
                + uid
                + "\npsw:"
                + psw
                + "\n\n\n以上两行冒号后分别写上学号密码，不要加空格/换行，谢谢\n\n请注意文件安全，不要放在明显位置\n\n可以从dailyFudan.exe创建快捷方式到桌面"
            )
            new.write(tmp)
        if verbose:
            print("账号已保存在目录下account.txt，请注意文件安全，不要放在明显位置\n\n建议拉个快捷方式到桌面")

    return uid, psw
