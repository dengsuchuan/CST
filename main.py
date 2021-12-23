# -*- coding: utf-8 -*-

import os
import requests
from subprocess import run
from subprocess import Popen, PIPE
import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射
 
    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        # sh = logging.StreamHandler()#往屏幕上输出
        sh = logging.FileHandler(filename,encoding='utf-8')#往文件里写入
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里

class Run(object):
  def getNetTime(self):
    try:
      self.logger.info('开始请求网络时间')
      head = {'User-Agent': 'Mozilla/5.0'}
      url = r'http://time1909.beijing-time.org/time.asp'
      # requests get
      try:
        r = requests.get(url,headers=head)
        r.encoding = 'utf-8'
        self.logger.info('请求网络时间成功')
      except Exception as e:
        self.logger.error('请求网络时间失败')
        self.logger.error(e)
        return False

      # 检查返回码
      if r.status_code == 200:
          result = r.text
          data = result.split(";")
          # ======================================================
          # 以下是数据文本处理：切割；
          year = data[1].split('=')[1]    # year=2021
          month = data[2].split('=')[1]
          day = data[3].split('=')[1]
          # wday = data[4].split('=')[1]
          hrs = data[5].split('=')[1]
          minute = data[6].split('=')[1]
          sec = data[7].split('=')[1]
          # ======================================================
          # timestr = "%s/%s/%s %s:%s:%s" % (year,month, day, hrs, minute, sec)
          # 将timestr转为时间戳格式
          # timestrp = time.mktime(time.strptime(timestr, "%Y/%m/%d %X"))

          date_str = "%s-%s-%s" % (year, month, day)
          time_str = "%s:%s:%s" % (hrs, minute, sec)
          return (date_str, time_str)
    except Exception as e:
      self.logger.error('网络时间获取失败')
      self.logger.error(e)
      return (-1)


if __name__ == '__main__':
  log = Logger('E:/Users/dengs/Documents/LOG/run.log',level='info')
  log.logger.info('************************程序启动************************')

  try:
    date_str, time_str = Run.getNetTime(log)
    devnull = open(os.devnull, 'wb')
    shell = run('date {} && time {}'.format(date_str, time_str), shell=True,stdout=PIPE, stderr=PIPE,stdin=devnull)
    if date_str == -1:
      log.logger.error('网络时间获取失败')
    else:
      log.logger.info('网络时间获取成功')
      log.logger.info(date_str)
      log.logger.info(time_str)
    log.logger.info(shell)
  except Exception as e:
    log.logger.error('程序出错')
    log.logger.error(e)
