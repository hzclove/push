# -*- coding: utf8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys
import os
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append(os.getcwd()+'/app/getui_sdk')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
