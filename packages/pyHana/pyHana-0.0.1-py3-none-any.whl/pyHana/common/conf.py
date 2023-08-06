import os
import configparser

# 설정파일 읽기
configPath = os.environ['PyhanaConfigPath']
config = configparser.ConfigParser()    
config.read(configPath+'/config.ini', encoding='utf-8') 

ebestId  = config['ebest']['id']
ebestPwd = config['ebest']['pwd']
certPwd  = config['ebest']['certpwd']
xingAPIRes = config['ebest']['xingAPIRes']

basePath = config['path']['base']
dartPath = config['path']['dart']
ecoIndexPath = config['path']['ecoIndex']
stockTradePath = config['path']['stockTrade']