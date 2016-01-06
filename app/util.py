# -*- coding: utf8 -*-
from .models import *
from xiaomi_push import xiaomi_push_message, xiaomi_daily_result, xiaomi_push_result
from getui_push import getui_push_message, getui_daily_result, getui_push_result
from umeng_push import umeng_push_message, umeng_push_result
from app import app
import math
import Queue
import threading

def err_log(error_data):
    '''输出错误日志'''
    lock = threading.Lock()
    lock.acquire()
    try:
        log_file = app.config['LOG_FILE']
        with open(log_file, 'a') as f:
            f.write(error_data)
    finally:
        lock.release()

def select_users(province_name, major_name, is_register, iOS_version, Android_version, is_all):
    '''根据条件筛选用户的clientId，返回字典
       有友盟号并且不为小米手机，或者有友盟号没有小米号的，用友盟推送
       剩下的，有小米的用小米推送
       再剩下的，用个推推送
    Args：
        province_name：省名，中文
        major_name：专业名，中文
        is_register：注册状态，0为未注册用户，1为注册用户，2为注册用户加非注册用户
        iOS_version：苹果版本
        Android_version：安卓版本
        is_all：全部用户传all，否则传空
    '''
    query = Client.query
    if is_all != 'all':
        if is_register == '1': #注册用户
            query = query.join(Account, Account.imei == Client.imei)
            if province_name != '全部':
                query = query.filter(Account.provinceName == province_name)
            if major_name != '全部':
                query = query.filter(Account.majorName == major_name)
        elif is_register == '0': #未注册用户
            query = query.outerjoin(Account, Account.imei == Client.imei).filter(Account.imei == None)
        #若版本选全部，前端传来的列表中会加个''，把appVersion为空的也查出来
        query = query.filter(or_(and_(Client.appVersion.in_(iOS_version.split(',')), Client.deviceOS.like('iOS%')), 
                                 and_(Client.appVersion.in_(Android_version.split(',')), Client.deviceOS.like('android%'))))
                             
    clients = query.all()
    cids = {'getui':[], 'xiaomi':[], 'umeng_iOS':[], 'umeng_android':[]}
    mi_mobiles = ['M1', 'M3S', 'm1_note', 'm2_note', 'm2', 'm1_metal']
    for c in clients:
        #有友盟号并且不为小米手机，或者有友盟号没有小米号的，用友盟推送
        if c.umengPushId and (not (c.mobileModel.lower().startswith('mi') or c.mobileModel.split(';')[0] in mi_mobiles) or not c.xiaomiPushId):
            if c.deviceOS.startswith('android'):
                cids['umeng_android'].append(c.umengPushId)
            # elif c.deviceOS.startswith('iOS'):
            else:  #目前将diviceOS为空的当做苹果
                cids['umeng_iOS'].append(c.umengPushId)
        elif c.xiaomiPushId:
            cids['xiaomi'].append(c.xiaomiPushId)
        elif c.getuiPushId:
            cids['getui'].append(c.getuiPushId)
            
    return cids

class PushThreadPool(object):
    """推送消息的线程池"""
    def __init__(self, target, basic_id, content, begin, end):
        '''
        Args：
            target：待推送的CID，{'getui':[], 'xiaomi':[], 'umeng_iOS':[], 'umeng_android':[]}
            basic_id: push_basic表中对应此推送的id
            content：透传消息，类型;标题;描述;id;课程类型
            begin：定时发送时间，%Y-%m-%d %H:%M:%S
            end：过期时间，%Y-%m-%d %H:%M:%S
        '''
        push_queue = self.grouping(target)
        thread_num = push_queue.qsize() if push_queue.qsize() <= 100 else 100
        self.thread_pool = [threading.Thread(target=self.push_message,args=[push_queue, basic_id, content, begin, end]) for i in range(thread_num)]

    def run(self):
        for t in self.thread_pool:
            t.setDaemon(True)
            t.start()

    def grouping(self, target):
        '''根据各平台的一次推送数量限制，将CID分组'''
        platform_limit = {'getui': 100,
                          'xiaomi': 1000,
                          'umeng_android': 5000,
                          'umeng_iOS': 5000}
        push_queue = Queue.Queue()
        for key in target:
            limit = platform_limit[key]
            raw = target[key]
            group_num = int(math.ceil(len(raw)/float(limit)))
            for g in range(group_num):
                push_queue.put({key:raw[g*limit:(g+1)*limit] if len(raw[g*limit:]) > limit else raw[g*limit:]})
        return push_queue



    def push_message(self, push_queue, basic_id, content, begin, end):
        '''调用三个推送平台的推送函数，返回各自的推送消息ID
        Args:
            push_queue：推送队列，保存待推送的一组组CID
            basic_id: push_basic表中对应此推送的id
            content：透传消息，类型;标题;描述;id;课程类型
            begin：定时发送时间，%Y-%m-%d %H:%M:%S
            end：过期时间，%Y-%m-%d %H:%M:%S
        '''
        
        while push_queue.qsize():
            try:
                target = push_queue.get(block=False)
            except Queue.Empty:
                return

            if 'getui' in target:
                result = getui_push_message(target['getui'], content, begin, end)
            elif 'xiaomi' in target:
                result = xiaomi_push_message(target['xiaomi'], content, begin, end)
            elif 'umeng_android' in target:
                result = umeng_push_message('android', target['umeng_android'], content, begin, end)
            elif 'umeng_iOS' in target:
                result = umeng_push_message('iOS', target['umeng_iOS'], content, begin, end)
                
            try:  
                push_ids = Push_ids(basic_id=basic_id, push_id=result['contentId'], source=target.keys()[0])
                db.session.add(push_ids)
                db.session.commit()
            except:  #若推送发生错误，result中将不包含contentId，通过捕获keyValue异常来打印错误日志
                error_data = 'push error, basic_id:{id}, platform:{platform}, error_msg:{error}\n' \
                             .format(id=basic_id, platform=target.keys()[0], error=result)
                err_log(error_data)

class PushResult(object):
    """根据推送平台返回的push_id查询推送的统计数据，同一次推送（相同basic_id）的统计数据可以相加"""
    def __init__(self, basic_id, source, push_id):
        '''
        Args：
            basic_id：push_basic表中对应此推送的id
            source：查询类别，[umeng_iOS|umeng_android|xiaomi|getui]
            push_id：推送平台返回的push_id
        '''
        self.basic_id = basic_id
        self.source = source
        self.push_id = push_id

    def get_result(self):
        '''根据推送平台返回的push_id查询推送的统计数据，失败次数超过三次则返回数据为0，同时记录到错误日志'''
        data = {'total_count': 0,
                'receive_count': 0,
                'click_count': 0}
        try_time = 0
        retry_time_limit = 3
        while try_time < 3:
            try:
                try_time += 1
                if self.source == 'getui':
                    result = getui_push_result(self.push_id)
                    data['total_count'] = result['msgTotal']
                    data['receive_count'] = result['msgProcess']
                    data['click_count'] = result['clickNum']
                elif self.source == 'xiaomi':
                    result = xiaomi_push_result(self.push_id)
                    data['total_count'] = result['resolved']
                    data['receive_count'] = result['delivered']
                    data['click_count'] = result['click']
                else:
                    result = umeng_push_result(self.source, self.push_id)
                    data['total_count'] = result['total_count']
                    data['receive_count'] = result['sent_count']
                    data['click_count'] = result['open_count']
            except Exception, e:
                if try_time >= 3:
                    error_data = 'statistic error, source:{source}, error_msg:{error}, platform_msg:{result}\n'.format(source=self.source, error=e, result=result)
                    err_log(error_data)
        self.statistic = data

    def get_json(self):
        '''返回前端json数据，包括该推送的基本信息和统计信息'''
        push_basic = Push_basic.query.get(self.basic_id)
        data = {key:value for key,value in push_basic.__dict__.items() if key != '_sa_instance_state'}
        return dict(data, **self.statistic)

    def __add__(self, other):
        '''相同basic_id，不同push_id的统计数据可以相加'''
        if self.basic_id == other.basic_id and self.push_id != other.push_id:
            result_sum = PushResult(self.basic_id, self.source, None)
            result_sum.statistic = {key: self.statistic[key] + other.statistic[key] for key in self.statistic}
            return result_sum
        else:
            raise TypeError

    def __str__(self):
        return 'basic_id:{basic_id}, source:{source}, push_id:{push_id}, statistic:{statistic}' \
                .format(basic_id=self.basic_id, source=self.source, push_id=self.push_id, statistic=self.statistic.__str__())

    def __repr__(self):
        return self.__str__()


class StatisticThreadPool(object):
    """获取推送统计结果的线程池"""
    def __init__(self, input_queue):
        '''
        Args：
            input_queue：多个PushResult对象
        '''
        self.input_queue = input_queue
        self.result_queue = Queue.Queue()
        thread_num = input_queue.qsize() if input_queue.qsize() <= 100 else 100
        self.thread_pool = [threading.Thread(target=self.push_statistic,args=[]) for i in range(thread_num)]

    def run(self):
        for t in self.thread_pool:
            t.start()
        for t in self.thread_pool:
            t.join()

    def push_statistic(self):
        while self.input_queue.qsize():
            try:
                target = self.input_queue.get(block=False)
            except Queue.Empty:
                return
            target.get_result()
            self.result_queue.put(target)

    def result(self):
        '''
        将result_queue中的统计数据按basic_id相加，输出一个json数据列表
        多次遍历result_list，将其中的元素相加求和。每一次遍历会将basic_id相同的元素相加，同时从原列表中删除；basic_id不同的元素相加时会报错，pass。
        有多少个不同的basic_id，就会循环几次
        '''
        result_list = []
        while self.result_queue.qsize():
            result_list.append(self.result_queue.get())
            
        sum_list = []
        while result_list:
            result_sum = result_list.pop(0)
            for r in result_list[:]:
                try:
                    result_sum += r
                    result_list.remove(r)
                except TypeError:
                    pass
            sum_list.append(result_sum.get_json())
        return sum_list