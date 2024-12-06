__all__=["dbcfg"]

import os,json

配置目录=[]
dh,_=os.path.splitdrive(os.getcwd())
配置目录.append(os.path.join(dh,"/etc","dbconn.config.d"))

class dbcfg(object):
    'dbcfg主类'
    def __init__(self,连接名='',ehm=0):
        self.ehm=ehm
        self.读配置文件(连接名)
        self.connected=False

    def 读配置文件(self,连接名):
        self.connectname=连接名
        for 目录 in 配置目录:
            配置文件=os.path.join(目录,f"{连接名}.cfg")
            if os.path.isfile(配置文件):
                self.配置数据=json.loads(open(配置文件).read())
                return
        self.q(-1,{"连接名":连接名})
        
    def cfg(self,实例=''):
        for 配置 in self.配置数据:
            if 实例==配置.get("name",""):
                return 配置
        self.q(-2,{"实例":实例})
    def connect(self,实例=''):
        默认包={"oracle":"cx_Oracle","mysql":"pymysql","sqlserver":"pytds","tds":"pytds"}
        import importlib
        cfg=self.cfg(实例)
        self.dbname=cfg["db"]
        if "python" not in cfg or "import" not in cfg["python"]:
            包=默认包.get(cfg["db"],cfg["db"])
        else:
            包=cfg["python"]["import"]
        try:
            m=importlib.import_module(包)
        except:
            return self.q(-4,{"name":包})
        try:
            self.conn=m.connect(*cfg["t"],**cfg["d"])
            self.connected=True
        except:
            return self.q(-5)
        else:
            return self.conn

    def q(self,返回码,参数={}):
        消息表={
            -1: "未找到配置文件{连接名}.cfg",
            -2:"配置文件中未找到实例{实例}",
            -3:"配置文件中需要设置python相关内容",
            -4:"import {name}错误",
            -5:"连接到数据库错误"
        }
        self.rtcode=返回码
        self.rtinfo=消息表.get(返回码,"错误的返回码").format(**参数)
        if self.ehm==1:
            print(self.rtinfo)
        if self.ehm==2:
            raise Exception(self.rtinfo)
        return self.rtcode
    def commit(self):
        self.conn.commit()
    def execute(self,ssql,*args,**kwargs):
        c=self.conn.cursor()
        c.execute(ssql,*args,**kwargs)
        return c
    def jg1(self,ssql,*args,**kwargs):
        '''根据sql返回1条结果'''
        c=self.conn.cursor()
        c.execute(ssql,*args,**kwargs)
        jg=c.fetchone()
        c.close()
        if jg==None:
            return
        if len(jg)==1:
            return jg[0]
        else:
            return jg
    def xg(self,ssql,*args,**kwargs):
        '''主要用于修改，执行完后附加commit操作'''
        c=self.execute(ssql,*args,**kwargs)
        self.commit()
        return c
    def test(self):     #通过获取当前时间来测试数据库是否工作正常
        if self.dbname.lower()=="oracle":
            print(self.jg1("select sysdate from dual"))
    def __getattribute__(self,name):
        if name in ("读配置文件","connect"):
            self.code=0
            self.info=""
        if name in ("c","conn") and not self.connected:
            self.connect()
        return object.__getattribute__(self,name)
