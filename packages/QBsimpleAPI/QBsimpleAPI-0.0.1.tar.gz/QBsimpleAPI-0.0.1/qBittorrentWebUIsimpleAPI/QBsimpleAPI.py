import json,requests,os
from datetime import datetime as dt
from bs4 import BeautifulSoup
class Byte_to_speed:
    def __init__(self,byte:int) -> None:
        self.byte=byte
        '''下载字节速度'''
        unit="B/s"
        if byte>1024:
            byte>>=10
            unit="KB/s"
        if byte>1024:
            byte>>=10
            unit="MB/s"
        self.speed=byte
        '''下载速度'''
        self.unit=unit
        '''下载速度单位'''
class login_qb:
    def __init__(self,port:int,login_user:str,login_passwd:str) -> None:
        '''
        port:qb web ui 端口\\
        login_user:登录用户名\\
        login_passwd:登录密码
        '''
        login_data={
            "username":login_user,
            "password":login_passwd
        }
        self.__port=str(port)
        self.__login_url=f"http://localhost:{(self.__port)}/api/v2/auth/login"
        self.__get_setting_url=f"http://localhost:{(self.__port)}/api/v2/app/preferences"
        self.__set_setting_url=f"http://localhost:{(self.__port)}/api/v2/app/setPreferences"
        self.__add_torrent_url=f"http://localhost:{self.__port}/api/v2/torrents/add"
        self.__get_download_infor_url=f"http://localhost:{self.__port}/api/v2/sync/maindata"
        self.__session=requests.session()
        login=self.__session.post(url=self.__login_url,data=login_data)
        if login.status_code==200:
            self.__user_setting=json.loads(self.__session.get(url=self.__get_setting_url).text)
        self.__add_torrent_setting={
            "autoTMM": self.__user_setting["auto_tmm_enabled"],
            "savepath": self.__user_setting["save_path"],
            "rename": "",
            "category": "",
            "paused": False,
            "stopCondition": None,
            "contentLayout": "Original",
            "dlLimit": float('nan'),
            "upLimit": float('nan')
        }
    def set_default_download_path(self,path:str):
        '''设置默认保存路径\\
        path:保存文件路径'''
        if os.path.exists(path=path):
            self.__user_setting["save_path"]=path
            self.__session.post(url=self.__set_setting_url,data={"json":json.dumps(self.__user_setting)})
        else:
            raise ValueError("路径错误")
    def add_download_torrent(self,path:str):
        '''添加bt种子文件\\
        path:种子文件路径'''
        if os.path.exists(path=path):
            with open(path,"rb") as r:
                torrent_bit=r.read()
            name=os.path.split(path)[1]
            files={"fileselect[]":(name,torrent_bit,'application/x-bittorrent')}
            self.__session.post(url=self.__add_torrent_url,data=self.__add_torrent_setting,files=files)
        else:
            raise ValueError("路径错误")
    def __get_download_infor(self) -> dict:
        '''获取下载信息'''
        return json.loads(self.__session.get(url=self.__get_download_infor_url).text)
    def get_download_speed(self) -> Byte_to_speed:
        '''获取下载速度\\
        返回一个类对象'''
        tmp=self.__get_download_infor()["server_state"]["dl_info_speed"]
        return Byte_to_speed(tmp)
    def __get_download_project(self):
        '''获取下载项目的信息hash值'''
        tmp:dict=self.__get_download_infor()["torrents"]
        tmp_keys=list(tmp.keys)
        return tmp_keys
    def test_json(self,json_str:dict or list):
        '''将json文本保存至文件'''
        with open(f"{dt.now().day}.json","w",encoding="utf-8") as w:
            json.dump(json_str,w,indent=4,ensure_ascii=False)