#!/usr/bin/python
# -*- coding: utf8 -*-
from flask import render_template, request, jsonify
from app import app, db
from util import *
from .models import *
import datetime
import Queue
import threading

@app.route('/pushpage')
def pushpage():
    return render_template('pushpage.html')

@app.route('/pushlist')
def pushlist():
    return render_template('pushlist.html')

@app.route('/push', methods=['POST'])
def push():
    '''推送信息
    Args:
        province_name：中文
        major_name：中文
        is_register：注册用户传1，非注册用户传空
        iOS_version：三个.分割，如1.0.4.0
        Android_version：两个.分割，如1.0.0
        article_type：资讯、社区或课程
        title
        description
        article_id
        begin：定时发送时间，默认为空 %Y-%m-%d %H:%M
        end：过期时间，默认为空 %Y-%m-%d %H:%M
        target：全部用户传all，默认为空
        course_type：课程类型[直买、录买、直列、直播、直回、录播]
    '''
    # target = {'getui':['dc03a22818ca65ea8b3ee0ef88b52122'],
    #           'xiaomi':[],
    #           'umeng_iOS':[],
    #           'umeng_android':[]}

    form = request.form
    for key,value in form.items():
        print key+': '+value
    province_name = form['province_name']
    major_name = form['major_name']
    is_register = form['is_register']
    iOS_version = form['iOS_version']
    Android_version = form['Android_version']
    article_type = form['article_type']
    title = form['title']
    description = form['description']
    article_id = form['article_id']
    begin = form['begin']
    end = form['end']
    course_type = form['course_type']
    is_all = form['target']
    #透传信息，课程类型course_type为以后做兼容，不影响现在的使用
    content = '{article_type};{title};{description};{article_id};{course_type}' \
              .format(article_type=article_type, title=title, description=description, article_id=article_id, course_type=course_type)
    if begin:
        begin += ':00'
    else:
        begin = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    push_time = datetime.datetime.strptime(begin, "%Y-%m-%d %H:%M:%S")
    if end:
        end += ':00'
        expire_time = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
    else:
        expire_time = push_time + datetime.timedelta(days = 3)
        end = datetime.datetime.strftime(expire_time, "%Y-%m-%d %H:%M:%S")

    target = select_users(province_name, major_name, is_register, iOS_version, Android_version, is_all)

    print len(target['xiaomi'])
    print len(target['umeng_iOS'])
    print len(target['umeng_android'])
    print len(target['getui'])

    push_basic = Push_basic(article_type=article_type, title=title, description=description, article_id=article_id, course_type=course_type,
                push_time=begin, expire_time=end, android_version=Android_version, iOS_version=iOS_version, is_all=is_all,
                province_name=province_name, major_name=major_name, register_type=is_register)
    db.session.add(push_basic)
    db.session.commit()
    basic_id = push_basic.id
    

    push_thread_pool = PushThreadPool(target, basic_id, content, begin, end)
    push_thread_pool.run()

    return jsonify({'result':'true'})


@app.route('/statistic')
def statistic():
    '''获取小米、个推、友盟begin到end间的单条推送统计数据
    Args:
        begin：查询起始日期，%Y-%m-%d
        end：查询结束日期，%Y-%m-%d 
        source: 查询类别，[total|umeng_iOS|umeng_android|xiaomi|getui]
    '''
    begin = request.args.get('begin')
    end = request.args.get('end')
    source = request.args.get('source', 'total')
    if end:
        end = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days = 1)
    else:
        end = datetime.datetime.now().date() + datetime.timedelta(days = 1)
    if begin:
        begin = datetime.datetime.strptime(begin, "%Y-%m-%d")
    else:
        begin = end - datetime.timedelta(days = 6)

    input_queue =  Queue.Queue()
    push_basics = Push_basic.query.filter(Push_basic.push_time >= begin, Push_basic.push_time <= end).all()
    for basic in push_basics:
        query = Push_ids.query.filter(Push_ids.basic_id == basic.id)
        if source != 'total':
            query = query.filter(Push_ids.source == source)
        push_ids = query.all()
        for push in push_ids:
            input_queue.put(PushResult(basic.id, push.source, push.push_id))

    thread_pool = StatisticThreadPool(input_queue)
    thread_pool.run()
    result = thread_pool.result()

    return jsonify({'result': 'true', 'msg': result})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/majors')
def get_majors():
    '''根据省份获取该省具有的专业，若上传省份为‘全部’，返回所有专业
    Args:
        province_name : 省份名，中文
    '''
    province_name = request.args.get('province_name','')
    if province_name and province_name != '全部':
        majors = Major.query.with_entities(Major.major_name).filter(Major.province_name == province_name).distinct()
    elif province_name:
        majors = Major.query.with_entities(Major.major_name).distinct()
    majors = ['全部'] + [m.major_name for m in majors]
    return jsonify({'result':'true', 'msg': majors})


@app.route('/provinces')
def get_provinces():
    '''获取所有省份名'''
    provinces = Province.query.all()
    provinces = ['全部'] + [p.province_name for p in provinces]
    return jsonify({'result':'true', 'msg':provinces})


@app.route('/versions')
def get_versions():
    '''获取安卓/iOS所有版本号'''
    versions = Client.query.with_entities(Client.appVersion).distinct()
    android = ['全部'] + sorted([v.appVersion for v in versions if len(v.appVersion.split('.'))==4])
    iOS = ['全部'] + sorted([v.appVersion for v in versions if len(v.appVersion.split('.'))==3]) + ['Bate1.1']
    return jsonify({'result':'true', 'msg':{'android':android, 'iOS':iOS}})

@app.route('/test')
def test():
    target = ['dc03a22818ca65ea8b3ee0ef88b52122']
    content = '资讯;口袋自考;安徽省开始;394'
    begin = "";
    end = "";
    print target
    print getui_push_message(target, content, begin, end)
    return jsonify({'result':'true'})