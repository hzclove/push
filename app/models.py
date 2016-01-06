# -*- coding: utf8 -*-
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import *
from sqlalchemy.dialects import mysql


class Account(db.Model):
    __tablename__ = 'account'
    __table_args__ = {'schema': 'study'}

    uid = db.Column('uid', VARCHAR(collation=u'utf8mb4_bin', length=128), primary_key=True, nullable=False, default='')
    nickname = db.Column('nickname', VARCHAR(collation=u'utf8mb4_bin', length=32), nullable=False, default='')
    passWord = db.Column('passWord', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    phone = db.Column('phone', VARCHAR(collation=u'utf8mb4_bin', length=32), nullable=False, default='')
    profileUrl = db.Column('profileUrl', VARCHAR(collation=u'utf8mb4_bin', length=256), nullable=False, default='')
    registerTime = db.Column('registerTime', TIMESTAMP(), nullable=False, default=func.current_timestamp())
    accountType = db.Column('accountType', VARCHAR(collation=u'utf8mb4_bin', length=32), nullable=False, default='')
    gender = db.Column('gender', VARCHAR(collation=u'utf8mb4_bin', length=32), nullable=False, default='DEFAULT')
    registerChannel = db.Column('registerChannel', VARCHAR(collation=u'utf8mb4_bin', length=110))
    qqToken = db.Column('qqToken', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    weixinToken = db.Column('weixinToken', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    weiboToken = db.Column('weiboToken', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    imei = db.Column('imei', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    provinceId = db.Column('provinceId', VARCHAR(collation=u'utf8mb4_bin', length=20), nullable=False, default='')
    provinceName = db.Column('provinceName', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    majorId = db.Column('majorId', VARCHAR(collation=u'utf8mb4_bin', length=20), nullable=False, default='')
    majorName = db.Column('majorName', VARCHAR(collation=u'utf8mb4_bin', length=128), nullable=False, default='')
    subjectId = db.Column('subjectId', VARCHAR(collation=u'utf8mb4_bin', length=512), nullable=False, default='')
    subjectName = db.Column('subjectName', VARCHAR(collation=u'utf8mb4_bin', length=512), nullable=False, default='')

class Client(db.Model):
    __tablename__ = 'client'
    __table_args__ = {'schema': 'study'}

    imei = db.Column('imei', VARCHAR(length=128), primary_key=True, nullable=False, default='')
    getuiPushId = db.Column('getuiPushId', VARCHAR(length=128), nullable=False, default='')
    xiaomiPushId = db.Column('xiaomiPushId', VARCHAR(length=128), nullable=False, default='')
    umengPushId = db.Column('umengPushId', VARCHAR(length=128), nullable=False, default='')
    mobileModel = db.Column('mobileModel', VARCHAR(length=128), nullable=False, default='')
    appVersion = db.Column('appVersion', VARCHAR(length=128), nullable=False, default='')
    deviceOS = db.Column('deviceOS', VARCHAR(length=128), nullable=False, default='')
    net = db.Column('net', VARCHAR(length=128), nullable=False, default='WIFI')
    lastLaunchTime = db.Column('lastLaunchTime', DATETIME(), nullable=False, default=func.current_timestamp())

class Province(db.Model):
    __tablename__ = 'province'
    __table_args__ = {'schema': 'study'}

    province_id = db.Column('province_id', VARCHAR(length=20), primary_key=True, nullable=False)
    province_name = db.Column('province_name', VARCHAR(length=50), nullable=False)

class Major(db.Model):
    __tablename__ = 'major'
    __table_args__ = {'schema': 'study'}

    province_name = db.Column('province_name', VARCHAR(length=20), nullable=False, primary_key=True)
    major_name = db.Column('major_name', VARCHAR(length=50), nullable=False)
    major_id = db.Column('major_id', VARCHAR(length=20), nullable=False, primary_key=True)
    major_stage = db.Column('major_stage', VARCHAR(length=20), nullable=False, default='')
    major_university = db.Column('major_university', VARCHAR(length=50), nullable=False, default='')
    subject_seq = db.Column('subject_seq', VARCHAR(length=20), nullable=False)
    subject_name = db.Column('subject_name', VARCHAR(length=50), nullable=False)
    subject_id = db.Column('subject_id', VARCHAR(length=20), primary_key=True)
    exam_mode = db.Column('exam_mode', VARCHAR(length=20))
    exam_type = db.Column('exam_type', VARCHAR(length=100))
    subject_property = db.Column('subject_property', VARCHAR(length=20))
    exam_month = db.Column('exam_month', VARCHAR(length=20))
    book_name = db.Column('book_name', VARCHAR(length=50))
    book_author = db.Column('book_author', VARCHAR(length=50))
    book_publisher = db.Column('book_publisher', VARCHAR(length=50))
    book_version = db.Column('book_version', VARCHAR(length=50))
    book_channel = db.Column('book_channel', VARCHAR(length=50))
    book_id = db.Column('book_id', VARCHAR(length=50))
    remark = db.Column('remark', TEXT())
    wenli_flag = db.Column('wenli_flag', VARCHAR(length=20))

class Push_basic(db.Model):
    __tablename__ = 'push_basic'
    __table_args__ = {'schema': 'sun'}
    __bind_key__ = 'push'

    id = db.Column('id', mysql.INTEGER(display_width=11), primary_key=True)
    article_type = db.Column('article_type', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    title = db.Column('title', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    description = db.Column('description', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    article_id = db.Column('article_id', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    course_type = db.Column('course_type', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    push_time = db.Column('push_time', TIMESTAMP(), nullable=False, default=func.current_timestamp())
    expire_time = db.Column('expire_time', TIMESTAMP(), nullable=False)
    android_version = db.Column('android_version', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    iOS_version = db.Column('iOS_version', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    is_all = db.Column('is_all', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    province_name = db.Column('province_name', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    major_name = db.Column('major_name', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    register_type = db.Column('register_type', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))

class Push_ids(db.Model):
    __tablename__ = 'push_ids'
    __table_args__ = {'schema': 'sun'}
    __bind_key__ = 'push'

    basic_id = db.Column('basic_id', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))
    push_id = db.Column('push_id', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255), primary_key=True)
    source = db.Column('source', VARCHAR(collation=u'utf8mb4_unicode_ci', length=255))