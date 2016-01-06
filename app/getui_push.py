# -*- coding: utf-8 -*-

from igt_push import *
from igetui.template.igt_transmission_template import *
from igetui.igt_message import *
from igetui.igt_target import *
import os
import hashlib
import urllib, urllib2, json
import time

#toList接口每个用户返回用户状态开关,true：打开 false：关闭
os.environ['needDetails'] = 'false'
APPKEY = "btWcHoswWV8RSCsxHZmru1"
APPID = "hZDj1lBJehA2BWN1ht5Wp"
MASTERSECRET = "Zr7bQaoDTL6dQWrFQw5Ju3"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'
push = IGeTui(HOST, APPKEY, MASTERSECRET)

def getui_push_message(target, content, begin, end):
    '''个推消息推送接口
    Args:
        target: Cid列表，不超过100个
        content: 透传消息，类型;标题;描述;id;课程类型
        begin: 定时发送时间，%Y-%m-%d %H:%M:%S
        end: 消息过期时间，%Y-%m-%d %H:%M:%S
    '''
    template = TransmissionTemplate()
    template.transmissionType = 2
    template.appId = APPID
    template.appKey = APPKEY
    template.transmissionContent = content
    if begin:
        if not end:
            end = time.localtime(time.mktime(time.strptime(begin,'%Y-%m-%d %H:%M:%S')) + 1000 * 3600 * 72)
            end = time.strftime('%Y-%m-%d %H:%M:%S', end)
        template.setDuration(begin, end)  #设置定时推送时间和过期时间

    message = IGtListMessage()
    message.data = template
    message.pushNetWorkType = 0  #设置是否根据WIFI推送消息，1为wifi推送，0为不限制推送
    message.isOffline = True
    message.offlineExpireTime = 1000 * 3600 * 72
    try:
        contentId = push.getContentId(message)
    except Exception as e:
        return e
    
    targets = [Target() for i in range(len(target))]
    for i in range(len(target)):
        targets[i].appId, targets[i].clientId = APPID, target[i]
    try:
        ret = push.pushMessageToList(contentId, targets)   #个推SDK默认会失败重发3次
        return ret
    except Exception as e:
        return e
    


def getui_daily_result(date):
    '''个推按日期统计接口
    Args:
        date: %Y%m%d
    '''
    try:
        res = push.queryAppPushDataByDate(APPID, date)
        return res
    except ValueError: #个推不支持查询今天的数据
        return {'data': {'sendCount': 0}}
    

def getui_push_result(task_id):
    try:
        res = push.getPushResult(task_id)
        return res
    except Exception as e:
        raise ValueError(e)