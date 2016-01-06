# -*- coding: utf-8 -*-
import time
import json
import urllib2
import urllib


headers = {'Authorization': 'key=Ss4Zt4y1S2VjQmVpFOHeGA=='}
restricted_package_name = 'com.withustudy.koudaizikao'

def xiaomi_push_message(target, payload, begin, end):
    '''小米消息推送接口
    Args:
        target: Cid列表，不超过1000个
        payload: 透传消息，类型;标题;描述;id;课程类型
        begin: 定时发送时间，%Y-%m-%d %H:%M:%S
        end: 消息过期时间，%Y-%m-%d %H:%M:%S
    '''
    url = 'https://api.xmpush.xiaomi.com/v2/message/regid'
    key_infos = payload.split(';')
    category, title, description, notify_id = key_infos[0], key_infos[1], key_infos[2], key_infos[3]
    post_data = {'payload': payload,
                'restricted_package_name': restricted_package_name,
                'pass_through': 0,
                'title': title,
                'description': description,
                'notify_type': -1,
                'notify_id': notify_id,
                'registration_id': ','.join(target)}
    if category == '课程':
        post_data['extra.notify_effect'] = '1'
    if begin: 
        timeArray = time.strptime(begin, "%Y-%m-%d %H:%M:%S")
        time_to_send = int(time.mktime(timeArray)) * 1000
        post_data['time_to_send'] = time_to_send
    else:
        time_to_send = time.time() * 1000
    if end:
        timeArray = time.strptime(end, "%Y-%m-%d %H:%M:%S")
        expired_time = int(time.mktime(timeArray)) * 1000
        time_to_live = expired_time - time_to_send
        post_data['time_to_live'] = time_to_live
    post_body = urllib.urlencode(post_data)
    try_time = 0
    retry_time_limit = 3
    while True:
        try:
            req = urllib2.Request(url, post_body, headers)
            r = json.loads(urllib2.urlopen(req).read())
            if r.get('data', ''):
                push_id = r['data']['id']
                return {'contentId': push_id}
            else:
                return r   
        except urllib2.HTTPError,e:
            if try_time >= retry_time_limit:
                return e.reason,e.read()
            else:
                try_time += 1
        except urllib2.URLError,e:
            if try_time >= retry_time_limit:
                return e.reason,e.read()
            else:
                try_time += 0.3


def xiaomi_push_result(id):
    '''小米按pushid统计接口
    注意：未到定时推送时间的推送id查询会返回错误，错误码65028，并且小米平台上显示的定时推送并不全（可进行撤销的推送），只会显示前20个
    '''
    url = 'https://api.xmpush.xiaomi.com/v1/trace/message/status?msg_id='+id
    try:
        req = urllib2.Request(url, headers=headers)
        r = json.loads(urllib2.urlopen(req).read())
        return r['data']['data']
    except KeyError:
        if r['code'] == 65028:
            return{'resolved': 0,
                   'delivered': 0,
                   'click': 0}
    except Exception as e:
        if r:
            raise ValueError(r)
        else:
            raise ValueError(e)

def xiaomi_daily_result(begin, end):
    '''小米按日期统计接口，返回起始到终止时间内的推送统计数据
    Args：
        begin: %Y%m%d
        end: %Y%m%d
    '''
    url = 'https://api.xmpush.xiaomi.com/v1/stats/message/counters?start_date={begin}&end_date={end}&restricted_package_name={package}' \
            .format(begin=begin, end=end, package=restricted_package_name)
    req = urllib2.Request(url, headers=headers)
    return json.loads(urllib2.urlopen(req).read())

if __name__ == '__main__':
    # target = ['d//igwEhgBGCI2TG6lWqlC8ZNeTG3VCVGdEJp7kSCJ1SQGxgjla6zyMz5piBVmNwr BinvjzKvo5ILK7QoDbq/wrUX52jXAQ8P/Xm838j/I=']
    # payload = '社区;口袋自考;互联网大咖男神亲授，助你职场技能爆表！;776;'
    # time_to_send = '2015-12-04 14:26'
    # timeArray = time.strptime(a, "%Y-%m-%d %H:%M")
    # time_to_send = int(time.mktime(timeArray))*1000
    # xiaomi_push_message(target, payload, '', '')



    # registration_id = session.query(Account).filter(Account.nickname == '黄先森').first().clientId.
    # print registration_id
    # push_unicast()
    # url = 'https://feedback.xmpush.xiaomi.com/v1/feedback/fetch_invalid_regids'
    # headers = {'Authorization': 'key=Ss4Zt4y1S2VjQmVpFOHeGA=='} 
    # req = urllib2.Request(url, headers=headers)
    # r = urllib2.urlopen(req)
    # rid = 'd//igwEhgBGCI2TG6lWqlC8ZNeTG3VCVGdEJp7kSCJ2VC7J3iT0V0aTgyiKsPIStgUI4NZWSw1vy16BIyhWg dBtDeH9FW6DJHRiMfAcFns='
    # if rid in r.read():
    #     print 1
    # print 2
    # print r.read().decode('utf8').encode('gbk')
    # url = 'https://api.xmpush.xiaomi.com/v1/trace/message/status?msg_id=slm29b22449478117477YF'
    # req = urllib2.Request(url, headers=headers)
    # r = urllib2.urlopen(req)
    # print json.loads(r.read())
    print xiaomi_push_result('slm10b2245095802819941')