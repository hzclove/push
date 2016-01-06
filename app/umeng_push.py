#coding=utf-8
import time
import datetime
import hashlib
import json
import urllib2

iOS_appkey = '5608b1b167e58eea2300022a'
iOS_app_master_secret = 'ig8sundgrlkskyph6h7r2llfdi5vijti'
android_appkey = '55de7cdbe0f55aa1ff0012fa'
android_app_master_secret = 'tcqzvwebmgfqtxewtsb4ucevhsxox8c4'

def wrap_post_data(method, url, source, params):
    if source == 'iOS':
        params['appkey'] = iOS_appkey
        post_body = json.dumps(params)
        sign = md5('%s%s%s%s' % (method,url,post_body,iOS_app_master_secret))
    else:
        params['appkey'] = android_appkey
        post_body = json.dumps(params)
        sign = md5('%s%s%s%s' % (method,url,post_body,android_app_master_secret))
    return post_body, sign

def md5(s):
    m = hashlib.md5(s)
    return m.hexdigest()

def umeng_push_message(source, target, custom, start_time, expire_time):
    '''友盟消息推送接口
    Args:
        source: iOS或android
        target: Cid列表，不超过10M
        custom: 透传消息，类型;标题;描述;id;课程类型
        start_time: 定时发送时间，%Y-%m-%d %H:%M:%S
        expire_time: 消息过期时间，%Y-%m-%d %H:%M:%S
    '''
    key_infos = custom.split(';')
    category, title, content, item, course_type = key_infos[0], key_infos[1], key_infos[2], key_infos[3], key_infos[4]
    timestamp = int(time.time() * 1000)
    method = 'POST'
    url = 'http://msg.umeng.com/api/send'
    params = {'timestamp': timestamp,
              'description': content,
              'type': 'filecast',
              'policy': {}
            }
    res = upload_device_tokens(source, target)
    if res[0] == 'ok':
        params['file_id'] = res[1]
    else:
        return res
    if start_time:  #防止发送时间小于当前时间
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds = 10)
        start_time = datetime.datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S")
        params['policy']['start_time'] = start_time
    if expire_time:
        params['policy']['expire_time'] = expire_time
    if source == 'iOS':
        params['payload'] = {'aps': {'alert': content},
                             'category': category,
                             'title': title,
                             'content': content,
                             'item': item}
        if category == '课程':
            params['payload']['type'] = course_type
    else:
        params['payload'] = {'display_type': 'notification',
                             'body': {'ticker': content,
                                      'title': title,
                                      'text': content}}
        if category == '课程':
            params['payload']['body']['after_open'] = 'go_app'
        else:
            params['payload']['body']['after_open'] = 'go_custom'
            params['payload']['body']['custom'] = custom
    try_time = 0
    retry_time_limit = 3
    while True:
        try:
            post_body, sign = wrap_post_data(method, url, source, params)
            r = json.loads(urllib2.urlopen(url + '?sign='+sign, data=post_body).read())
            push_id = r['data']['task_id']
            return {'contentId': push_id}
        except urllib2.HTTPError,e:
            if try_time >= retry_time_limit:
                return e.reason,e.read()
            else:
                r = json.loads(e.read())
                if r['data']['error_code'] == '2002':  #定时发送时间不能小于当前时间
                    start_time = params['policy']['start_time']
                    start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes = 1)
                    start_time = datetime.datetime.strftime(start_time, "%Y-%m-%d %H:%M:%S")
                    params['policy']['start_time'] = start_time
                elif r['data']['error_code'] == '2003':  #过期时间不能小于定时发送时间
                    expire_time = params['policy']['expire_time']
                    expire_time = datetime.datetime.strptime(expire_time, "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days = 1)
                    expire_time = datetime.datetime.strftime(expire_time, "%Y-%m-%d %H:%M:%S")
                    params['policy']['expire_time'] = expire_time
                elif r['data']['error_code'] == '2026':  #时间戳过期
                    time.sleep(60)
                    timestamp = int(time.time() * 1000 )
                    params['timestamp'] = timestamp
                else:
                    try_time += 1
        except urllib2.URLError,e:
            if try_time >= retry_time_limit:
                return e.reason,e.read()
            else:
                try_time += 0.3
            

def upload_device_tokens(source, target):
    '''批量上传CID，返回文件id
    Args:
        source: iOS或android
        target: Cid列表，不超过10M
    '''
    timestamp = int(time.time() * 1000)
    method = 'POST'
    url = 'http://msg.umeng.com/upload'
    params = {'timestamp': timestamp,
              'content': '\n'.join(target)}
    post_body, sign = wrap_post_data(method, url, source, params)
    try_time = 0
    retry_time_limit = 3
    while True:
        try:
            r = json.loads(urllib2.urlopen(url + '?sign='+sign, data=post_body).read())
            return 'ok', r['data']['file_id']
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

def umeng_push_result(source, id):
    '''友盟按pushid统计接口
    Args:
        source: iOS或android
        id: push_id
    '''
    timestamp = int(time.time() * 1000 )
    method = 'POST'
    url = 'http://msg.umeng.com/api/status'
    params = {'timestamp': timestamp,
              'task_id': id}
    post_body, sign = wrap_post_data(method, url, source, params)
    try:
        r = json.loads(urllib2.urlopen(url + '?sign='+sign, data=post_body).read())
        return r['data']
    except urllib2.HTTPError,e:
        return e.reason,e.read()
    except urllib2.URLError,e:
        return e.reason

if __name__ == '__main__':
    device_tokens = ['At_9szPEGZjzd7udmDyZdXgClUIyR0euwZo1AcQAx2mY']
    category = '社区'
    title = '口袋自考'
    content = '互联网大咖男神亲授，助你职场技能爆表！'
    item = '776'
    start_time = ''
    end_time = ''
    custom = '资讯;口袋自考;安徽省开始;394;asdg'
    # umeng_push_message('android', device_tokens, custom, start_time, end_time)
    # upload_device_tokens(device_tokens)
    print umeng_push_result('android', 'uf21304145102502600000')
