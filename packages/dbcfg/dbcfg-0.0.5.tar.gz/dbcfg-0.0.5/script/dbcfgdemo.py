import sys

import dbcfg

def main():
    if len(sys.argv)<2:
        print("需要附加一个参数指定配置文件名")
        return
    dbc=dbcfg.use(sys.argv[1],ehm=1)    #读取xxx.cfg里的配置信息
    dbc.connect()
    print(dbc.dbname)
    cfg=dbc.cfg()           #返回指定名称的配置，不指定使用name为""的那一个
    print(cfg)
    dbc.test()
