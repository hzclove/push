注意：
若需要将服务切换到其他服务器上，需在友盟平台添加新服务器的ip，iOS和安卓需要分别添加

#安装所需的Python库
pip install -r requirements.txt

可能出现的报错信息：
No package 'libffi' found - fatal error: ffi.h: No such file or directory
解决方法：
yum install libffi libffi-devel

#start.sh
kill `cat rocket.pid` >/dev/null 2>&1
gunicorn app:app -p rocket.pid -b 0.0.0.0:8000 -D

#stop.sh
kill `cat rocket.pid` >/dev/null 2>&1