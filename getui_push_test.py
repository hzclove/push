# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd()+'/getui_sdk')
from app.getui_push import getui_push_message, getui_push_result


if __name__ == '__main__':
    target = ['0d7fa85c841c704cd6002b00ec1f868e']
    content = '资讯;口袋自考;安徽省开始;394;hhhhh'
    begin = "";
    end = "";
    print getui_push_message(target, content, begin, end)
     
    # rep = getPushResult("OSL-1207_gXrAlavD9s9fbQWqiU2a49")
    # print rep
    # print getui_daily_result('20151212')
	# id = 'OSL-1224_74uzvHpHKH77b5cfGr6ez5'
	# print getui_push_result(id)
    