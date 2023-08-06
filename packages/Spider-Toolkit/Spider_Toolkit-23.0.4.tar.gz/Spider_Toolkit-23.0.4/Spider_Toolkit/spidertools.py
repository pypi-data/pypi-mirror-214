from .tools import Download_byte
from .tools import Open_js
from .tools import Save
from .tools import Random_ua
from .filtering import Open_js_parameter_filtering
from .filtering import Save_parameter_filtering
from .filtering import Download_Byte_parameter_filtering
from .filtering import Random_ua_parameter_filtering


# byte下载器
def download_byte(
        Max_Thread: int = 0,
        Max_Rerty: int = 3,
        Time_Sleep: [float, int] = 0,
        Request_Timeout: [float, int] = 10,
        urls: list = None,
        headers: [dict[str, any], None] = None,
        cookie: [dict[str, any], None] = None,
        param: [dict[str, any], None] = None,
        data: [dict[str, any], None] = None,
        proxies: [dict[str, any], None] = None,
        verify: bool = True,
        path_: str = './',
        names: [list, None] = None,
        type_: str = '',
        Save_Error_Log: bool = True,
        Show_Progress_Bar: bool = False,
        Show_Error_Info: bool = True
):
    '''
    :param Max_Thread: 最大线程数
    :param Max_Rerty: 最大重试数
    :param Time_Sleep: 每轮休眠时间
    :param Request_Timeout: 请求超时时间
    :param urls: url列表或单个url
    :param headers: 请求头
    :param cookie: cookie
    :param param: param
    :param data: data
    :param proxies: 代理
    :param verify: verify
    :param path_: 保存路径
    :param names: 标题
    :param type_: 存储类型
    :param Save_Error_Log: 保存失败日志
    :param Show_Progress_Bar: 显示进度条
    :return: download_byte对象
    '''
    path_ = path_.replace('\\', '/')
    if path_[-1] != '/':
        path_ += '/'
    if Download_Byte_parameter_filtering.donwload_byte_filtering(
            Max_Thread=Max_Thread,
            Max_Rerty=Max_Rerty,
            Time_Sleep=Time_Sleep,
            Request_Timeout=Request_Timeout,
            urls=urls,
            headers=headers,
            cookie=cookie,
            param=param,
            data=data,
            proxies=proxies,
            verify=verify,
            path_=path_,
            names=names,
            type_=type_,
            Save_Error_Log=Save_Error_Log,
            Show_Progress_Bar=Show_Progress_Bar,
            Show_Error_Info=Show_Error_Info
    ):
        url_num = len(urls)
        url_list = []
        if type(headers) == list:
            headers = Download_byte.param_dispose(url_num, headers)
        if type(cookie) == list:
            cookie = Download_byte.param_dispose(url_num, cookie)
        if type(param) == list:
            param = Download_byte.param_dispose(url_num, param)
        if type(data) == list:
            data = Download_byte.param_dispose(url_num, data)
        if type(proxies) == list:
            proxies = Download_byte.param_dispose(url_num, proxies)
        if names == [] or names == None:
            if type_ == '':
                for u in urls:
                    if '?' not in u:
                        name_ = u.split('/')[-1].split('.')[0]
                        type__ = u.split('/')[-1].split('.')[1]
                    else:
                        name_ = u.split('?')[0].split('/')[-1].split('.')[0]
                        type__ = u.split('?')[0].split('/')[-1].split('.')[1]
                    url_ = {'url': u, 'name': name_, 'type': type__, 'num': 0}
                    if type(headers) == list:
                        if len(headers) != 1:
                            url_['header'] = headers[0]['t']
                            headers[0]['n'] = headers[0]['n'] - 1
                            if headers[0]['n'] == 0:
                                headers.pop(0)
                        else:
                            url_['header'] = headers[0]['t']
                    else:
                        url_['header'] = headers
                    if type(cookie) == list:
                        if len(cookie) != 1:
                            url_['cookie'] = cookie[0]['t']
                            cookie[0]['n'] = cookie[0]['n'] - 1
                            if cookie[0]['n'] == 0:
                                cookie.pop(0)
                        else:
                            url_['cookie'] = cookie[0]['t']
                    else:
                        url_['cookie'] = cookie
                    if type(param) == list:
                        if len(param) != 1:
                            url_['param'] = param[0]['t']
                            param[0]['n'] = param[0]['n'] - 1
                            if param[0]['n'] == 0:
                                param.pop(0)
                        else:
                            url_['param'] = param[0]['t']
                    else:
                        url_['param'] = param
                    if type(data) == list:
                        if len(data) != 1:
                            url_['data'] = data[0]['t']
                            data[0]['n'] = data[0]['n'] - 1
                            if data[0]['n'] == 0:
                                data.pop(0)
                        else:
                            url_['data'] = data[0]['t']
                    else:
                        url_['data'] = data
                    if type(proxies) == list:
                        if len(proxies) != 1:
                            url_['proxies'] = proxies[0]['t']
                            proxies[0]['n'] = proxies[0]['n'] - 1
                            if proxies[0]['n'] == 0:
                                proxies.pop(0)
                        else:
                            url_['proxies'] = proxies[0]['t']
                    else:
                        url_['proxies'] = proxies
                    url_list.append(url_)
            else:
                for u in urls:
                    if '?' not in u:
                        name_ = u.split('/')[-1].split('.')[0]
                        type__ = type_
                    else:
                        name_ = u.split('?')[0].split('/')[-1].split('.')[0]
                        type__ = type_
                    url_ = {'url': u, 'name': name_, 'type': type__, 'num': 0}
                    if type(headers) == list:
                        if len(headers) != 1:
                            url_['header'] = headers[0]['t']
                            headers[0]['n'] = headers[0]['n'] - 1
                            if headers[0]['n'] == 0:
                                headers.pop(0)
                        else:
                            url_['header'] = headers[0]['t']
                    else:
                        url_['header'] = headers
                    if type(cookie) == list:
                        if len(cookie) != 1:
                            url_['cookie'] = cookie[0]['t']
                            cookie[0]['n'] = cookie[0]['n'] - 1
                            if cookie[0]['n'] == 0:
                                cookie.pop(0)
                        else:
                            url_['cookie'] = cookie[0]['t']
                    else:
                        url_['cookie'] = cookie
                    if type(param) == list:
                        if len(param) != 1:
                            url_['param'] = param[0]['t']
                            param[0]['n'] = param[0]['n'] - 1
                            if param[0]['n'] == 0:
                                param.pop(0)
                        else:
                            url_['param'] = param[0]['t']
                    else:
                        url_['param'] = param
                    if type(data) == list:
                        if len(data) != 1:
                            url_['data'] = data[0]['t']
                            data[0]['n'] = data[0]['n'] - 1
                            if data[0]['n'] == 0:
                                data.pop(0)
                        else:
                            url_['data'] = data[0]['t']
                    else:
                        url_['data'] = data
                    if type(proxies) == list:
                        if len(proxies) != 1:
                            url_['proxies'] = proxies[0]['t']
                            proxies[0]['n'] = proxies[0]['n'] - 1
                            if proxies[0]['n'] == 0:
                                proxies.pop(0)
                        else:
                            url_['proxies'] = proxies[0]['t']
                    else:
                        url_['proxies'] = proxies
                    url_list.append(url_)
        else:
            if type_ == '':
                for i in range(url_num):
                    if '?' not in urls[i]:
                        name_ = names[i]
                        type__ = urls[i].split('/')[-1].split('.')[1]
                    else:
                        name_ = names[i]
                        type__ = urls[i].split('?')[0].split('/')[-1].split('.')[1]
                    url_ = {'url': urls[i], 'name': name_, 'type': type__, 'num': 0}
                    if type(headers) == list:
                        if len(headers) != 1:
                            url_['header'] = headers[0]['t']
                            headers[0]['n'] = headers[0]['n'] - 1
                            if headers[0]['n'] == 0:
                                headers.pop(0)
                        else:
                            url_['header'] = headers[0]['t']
                    else:
                        url_['header'] = headers
                    if type(cookie) == list:
                        if len(cookie) != 1:
                            url_['cookie'] = cookie[0]['t']
                            cookie[0]['n'] = cookie[0]['n'] - 1
                            if cookie[0]['n'] == 0:
                                cookie.pop(0)
                        else:
                            url_['cookie'] = cookie[0]['t']
                    else:
                        url_['cookie'] = cookie
                    if type(param) == list:
                        if len(param) != 1:
                            url_['param'] = param[0]['t']
                            param[0]['n'] = param[0]['n'] - 1
                            if param[0]['n'] == 0:
                                param.pop(0)
                        else:
                            url_['param'] = param[0]['t']
                    else:
                        url_['param'] = param
                    if type(data) == list:
                        if len(data) != 1:
                            url_['data'] = data[0]['t']
                            data[0]['n'] = data[0]['n'] - 1
                            if data[0]['n'] == 0:
                                data.pop(0)
                        else:
                            url_['data'] = data[0]['t']
                    else:
                        url_['data'] = data
                    if type(proxies) == list:
                        if len(proxies) != 1:
                            url_['proxies'] = proxies[0]['t']
                            proxies[0]['n'] = proxies[0]['n'] - 1
                            if proxies[0]['n'] == 0:
                                proxies.pop(0)
                        else:
                            url_['proxies'] = proxies[0]['t']
                    else:
                        url_['proxies'] = proxies
                    url_list.append(url_)
            else:
                for i in range(url_num):
                    url_ = {'url': urls[i], 'name': names[i], 'type': type_, 'num': 0}
                    if type(headers) == list:
                        if len(headers) != 1:
                            url_['header'] = headers[0]['t']
                            headers[0]['n'] = headers[0]['n'] - 1
                            if headers[0]['n'] == 0:
                                headers.pop(0)
                        else:
                            url_['header'] = headers[0]['t']
                    else:
                        url_['header'] = headers
                    if type(cookie) == list:
                        if len(cookie) != 1:
                            url_['cookie'] = cookie[0]['t']
                            cookie[0]['n'] = cookie[0]['n'] - 1
                            if cookie[0]['n'] == 0:
                                cookie.pop(0)
                        else:
                            url_['cookie'] = cookie[0]['t']
                    else:
                        url_['cookie'] = cookie
                    if type(param) == list:
                        if len(param) != 1:
                            url_['param'] = param[0]['t']
                            param[0]['n'] = param[0]['n'] - 1
                            if param[0]['n'] == 0:
                                param.pop(0)
                        else:
                            url_['param'] = param[0]['t']
                    else:
                        url_['param'] = param
                    if type(data) == list:
                        if len(data) != 1:
                            url_['data'] = data[0]['t']
                            data[0]['n'] = data[0]['n'] - 1
                            if data[0]['n'] == 0:
                                data.pop(0)
                        else:
                            url_['data'] = data[0]['t']
                    else:
                        url_['data'] = data
                    if type(proxies) == list:
                        if len(proxies) != 1:
                            url_['proxies'] = proxies[0]['t']
                            proxies[0]['n'] = proxies[0]['n'] - 1
                            if proxies[0]['n'] == 0:
                                proxies.pop(0)
                        else:
                            url_['proxies'] = proxies[0]['t']
                    else:
                        url_['proxies'] = proxies
                    url_list.append(url_)

        if len(urls) == 1 or Max_Thread == 0:
            return Download_byte.download_byte(
                Max_Thread=Max_Thread,
                Max_Rerty=Max_Rerty,
                Time_Sleep=Time_Sleep,
                Request_Timeout=Request_Timeout,
                url_list=url_list,
                verify=verify,
                path_=path_,
                Save_Error_Log=Save_Error_Log,
                Show_Progress_Bar=Show_Progress_Bar,
                Show_Error_Info=Show_Error_Info
            )
        else:
            return Download_byte.thread_download_byte(
                Max_Thread=Max_Thread,
                Max_Rerty=Max_Rerty,
                Time_Sleep=Time_Sleep,
                Request_Timeout=Request_Timeout,
                url_list=url_list,
                verify=verify,
                path_=path_,
                Save_Error_Log=Save_Error_Log,
                Show_Progress_Bar=Show_Progress_Bar,
                Show_Error_Info=Show_Error_Info
            )
    else:
        pass


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
    '''
        :param url: url
        :param headers: 请求头
        :param cookie: cookie
        :param param: param
        :param data: data
        :param proxies: 代理
        :param verify: verify
        :param path_: 保存路径
        :param name: 文件名
        :param type_: 存储类型
        :return: 字符串'ok'
    '''
    path_ = path_.replace('\\', '/')
    if path_[-1] != '/':
        path_ += '/'
    if name == '':
        try:
            if '?' in url:
                name = url.split('?')[0].split('/')[-1].split('.')[0]
            else:
                name = url.split('/')[-1].split('.')[0]
        except:
            raise '尝试切割url命名失败，请手动设置名称'
    if type_ == '':
        try:
            if '?' in url:
                type_ = url.split('?')[0].split('/')[-1].split('.')[1]
            else:
                type_ = url.split('/')[-1].split('.')[1]
        except:
            raise '尝试切割type文件类型失败，请手动设置名称'

    if Download_Byte_parameter_filtering.donwload_byte_function_filtering(
            url=url,
            headers=headers,
            cookie=cookie,
            param=param,
            data=data,
            proxies=proxies,
            verify=verify,
            path_=path_,
            name=name,
            type_=type_
    ):
        Download_byte.donwload_byte_function(
            url=url,
            headers=headers,
            cookie=cookie,
            param=param,
            data=data,
            proxies=proxies,
            verify=verify,
            path_=path_,
            name=name,
            type_=type_
        )
        return 'ok'
    else:
        pass


# 打开js文件
def open_js(
        path_: str = '',
        encoding: str = 'utf-8',
        cwd: any = None
):
    '''
    :param path_: 文件路径
    :param encoding: 编码方式
    :param cwd: cwd
    :return: execjs.compile对象,可以直接.call调用
    '''
    path_ = path_.replace('\\', '/')
    if Open_js_parameter_filtering.open_js_filtering(
            path_=path_,
            encoding=encoding,
            cwd=cwd
    ):
        return Open_js.open_js(path_, encoding, cwd)
    else:
        pass


# 数据写入csv
def save_to_csv(
        path_: str = '',
        file_name: str = '',
        data: list = None,
        mode: str = 'w',
        encoding: str = 'utf-8',
        errors=None,
        newline=''
):
    '''
        :param path_: 文件路径
        :param file_name: 保存文件名
        :param data: 保存的数据
        :param mode: 模式
        :param encoding: 编码方式
        :param errors: errors
        :param newline: newline
        :return: 字符串'ok'
    '''
    path_ = path_.replace('\\', '/')
    if path_[-1] != '/':
        path_ += '/'
    if '.csv' not in file_name:
        file_name = file_name + '.csv'

    if Save_parameter_filtering.save_to_csv_filtering(
            path_=path_,
            file_name=file_name,
            data=data,
            mode=mode,
            encoding=encoding,
            errors=errors,
            newline=newline
    ):
        Save.save_to_csv(path_=path_,
                         file_name=file_name,
                         data=data,
                         mode=mode,
                         encoding=encoding,
                         errors=errors,
                         newline=newline)
        return 'ok'
    else:
        pass


# 数据写入xlsx
def save_to_xlsx(
        path_: str = '',
        file_name: str = '',
        data: dict = None,
        mode: str = 'w',
        sheet_name: str = "Sheet1",
        columns: any = None,
        header: bool = True,
        index: bool = True
):
    '''
        :param path_: 文件路径
        :param file_name: 保存文件名
        :param data: 保存的数据
        :param mode: 模式
        :param sheet_name: 使用sheet的名字
        :param columns: columns
        :param header: header
        :param index: index
        :return: 字符串'ok'
    '''
    path_ = path_.replace('\\', '/')
    if path_[-1] != '/':
        path_ += '/'
    if '.xlsx' not in file_name:
        file_name = file_name + '.xlsx'

    if Save_parameter_filtering.save_to_xlsx_filtering(
            path_=path_,
            file_name=file_name,
            data=data,
            mode=mode,
            sheet_name=sheet_name,
            columns=columns,
            header=header,
            index=index
    ):
        Save.save_to_xlsx(
            path_=path_,
            file_name=file_name,
            data=data,
            mode=mode,
            sheet_name=sheet_name,
            columns=columns,
            header=header,
            index=index
        )
        return 'ok'
    else:
        pass


# 数据写入数据库
def save_to_mysql(
        host: str = 'localhost',
        port: int = 3306,
        user: str = 'root',
        password: str = '',
        database: str = '',
        charset: str = 'utf8'
):
    '''
        :param host: 主机
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库
        :param charset: 编码
        :return: save_to_mysql的对象,用完记得.close
    '''
    if Save_parameter_filtering.save_to_mysql_filtering(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset
    ):
        return Save.save_to_mysql(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset
        )
    else:
        pass


def save_to_redis(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        password: str = '',
        pool_size: int = 10
):
    '''
        :param host: 主机
        :param port: 端口
        :param password: 密码
        :param database: 数据库
        :param pool_size: 连接池大小
        :return: save_to_redis的对象,用完记得.close
    '''
    if Save_parameter_filtering.save_to_redis_filtering(
            host=host,
            port=port,
            database=database,
            password=password,
            pool_size=pool_size
    ):
        return Save.save_to_redis(
            host=host,
            port=port,
            database=database,
            password=password,
            pool_size=pool_size
        )
    else:
        pass


def save_to_mongo(
        host: str = 'localhost',
        port: int = 6379,
        database: str = '',
        user: str = '',
        password: str = '',
        pool_size: int = 10,
        collection: str = ''
):
    '''
        :param host: 主机
        :param port: 端口
        :param user: 用户
        :param password: 密码
        :param database: 数据库
        :param pool_size: 连接池大小
        :param collection: collection
        :return: save_to_mongo的对象,用完记得.close
    '''
    if Save_parameter_filtering.save_to_mongo_filtering(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            pool_size=pool_size,
            collection=collection
    ):
        return Save.save_to_mongo(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            pool_size=pool_size,
            collection=collection
        )
    else:
        pass


def random_ua(
        factory: str = 'random'
):
    '''
        :param factory: 指定浏览器厂家
        :return: 请求头
    '''
    if Random_ua_parameter_filtering.random_ua_filtering(
            factory=factory
    ):
        return Random_ua.random_ua(factory=factory)
    else:
        pass
