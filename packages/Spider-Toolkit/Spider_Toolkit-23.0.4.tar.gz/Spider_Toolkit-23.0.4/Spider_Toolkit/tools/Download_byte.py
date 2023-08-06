import sys
import time
import requests
import datetime
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from collections import deque


class download_byte():

    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [list, float, int] = 0,
            Request_Timeout: [float, int] = 10,
            url_list: list = None,
            path_: str = './',
            verify: bool = True,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
            Show_Error_Info: bool = True
    ):
        self.Max_Thread = Max_Thread
        self.Max_Rerty = Max_Rerty
        self.Time_Sleep = Time_Sleep
        self.Request_Timeout = Request_Timeout
        self.url_list = url_list
        self.path_ = path_
        self.verify = verify
        self.Save_Error_Log = Save_Error_Log
        self.Show_Progress_Bar = Show_Progress_Bar
        self.Show_Error_Info = Show_Error_Info
        self.url_queue = deque(maxlen=len(self.url_list) + 1)
        self.error_list = []
        for u in url_list:
            self.url_queue.append(u)
        self.all_task_num = self.url_queue.__len__() + 1

    def start(self):
        while bool(self.url_queue):
            self.get_(url_=self.url_queue.popleft())
            if self.Show_Progress_Bar:
                self.progress_bar(self.all_task_num - self.url_queue.__len__(), self.all_task_num)
            else:
                pass

    def get_(self, url_):
        try:
            respones = requests.get(url=url_['url'], headers=url_['header'], cookies=url_['cookie'],
                                    proxies=url_['proxies'],
                                    verify=self.verify, params=url_['param'], data=url_['data'],
                                    timeout=self.Request_Timeout)
            if respones.status_code == 200:
                self.save_(respones.content, url_['name'], url_['type'])
            else:
                raise Exception('响应码:{}，请求失败'.format(respones.status_code))
        except Exception as e:
            self.error_prompt(e, url_['url'])
        time.sleep(self.Time_Sleep)

    def error_prompt(self, e, url_):
        if url_['num'] < self.Max_Rerty:
            if self.Show_Error_Info:
                print('当前url：{}\n出现异常：{}\n未超出指定重试次数({}/{})，将添加回对列\n'.format(url_['url'], e, url_['num'] + 1,
                                                                            self.Max_Rerty))
            url_['num'] = url_['num'] + 1
            self.url_queue.append(url_)
        else:
            if self.Show_Error_Info:
                print('当前url：{}\n出现异常：{}\n超出指定重试次数({})，将写入错误列表\n'.format(url_['url'], e,
                                                                         self.Max_Rerty))
            self.error_list.append({'url': url_['url'], 'num': url_['num'] + 1, 'log': e})

    def save_(self, content_, name, type_):
        with open(self.path_ + name + '.' + type_, 'wb') as f:
            f.write(content_)

    def progress_bar(self, finish_tasks_number, all_task_number):
        percentage = round(finish_tasks_number / all_task_number * 100)
        print("\r下载进度: {}%: ".format(percentage), "▓" * (percentage // 2), end="")
        sys.stdout.flush()

    def save_log(self):
        with open(self.path_ + datetime.datetime.now().strftime("%Y年%m月%d日_%H时%M分%S秒") + '_log.txt', 'w',
                  encoding='utf-8') as f:
            for i in self.error_list:
                f.write(str(i) + '\n')


class thread_download_byte(download_byte):

    def __init__(
            self,
            Max_Thread: int = 0,
            Max_Rerty: int = 3,
            Time_Sleep: [list, float, int] = 0,
            Request_Timeout: [float, int] = 10,
            url_list: list = None,
            path_: str = './',
            verify: bool = True,
            Save_Error_Log: bool = True,
            Show_Progress_Bar: bool = False,
            Show_Error_Info: bool = True
    ):
        super(thread_download_byte, self).__init__(
            Max_Thread=Max_Thread,
            Max_Rerty=Max_Rerty,
            Time_Sleep=Time_Sleep,
            Request_Timeout=Request_Timeout,
            url_list=url_list,
            path_=path_,
            verify=verify,
            Save_Error_Log=Save_Error_Log,
            Show_Progress_Bar=Show_Progress_Bar,
            Show_Error_Info=Show_Error_Info
        )
        self.threadpool = ThreadPoolExecutor(max_workers=self.Max_Thread)

    def start(self):
        while bool(self.url_queue):
            self.all_task = []
            if self.url_queue.__len__() >= self.Max_Thread:
                for i in range(self.Max_Thread):
                    self.all_task.append(self.threadpool.submit(self.get_(url_=self.url_queue.popleft())))
                wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
            else:
                for i in range(self.url_queue.__len__()):
                    self.all_task.append(self.threadpool.submit(self.get_(url_=self.url_queue.popleft())))
                wait(self.all_task, return_when=ALL_COMPLETED, timeout=self.Request_Timeout)
            if self.Show_Progress_Bar:
                self.progress_bar(self.all_task_num - self.url_queue.__len__(), self.all_task_num)
            else:
                pass
        if self.Save_Error_Log and self.error_list != []:
            self.save_log()


def donwload_byte_function(
        url: str = None,
        headers: [dict[str, any], None] = None,
        cookie: [dict[str, any], None] = None,
        param: [dict[str, any], None] = None,
        data: [dict[str, any], None] = None,
        proxies: [dict[str, any], None] = None,
        verify: bool = True,
        path_: str = './',
        name: str = '',
        type_: str = ''
):
    respones = requests.get(url=url, headers=headers, cookies=cookie, proxies=proxies,
                            verify=verify, params=param, data=data)
    if respones.status_code == 200:
        with open(path_ + name + '.' + type_, 'wb') as f:
            f.write(respones.content)
    else:
        raise Exception('响应码:{}，请求失败'.format(respones.status_code))


def param_dispose(
        num:int,
        param_: list
)-> list:
        n = int(num / len(param_))
        for h in range(len(param_)):
            param_[h] = {'t': param_[h], 'n': n}




