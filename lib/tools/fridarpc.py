import os
import time
# import argparse
from lamda.client import *



def run_frida():
    cert = os.environ.get("CERTIFICATE", None)
    port = int(os.environ.get("PORT", 65000))

    d = Device("192.168.121.231", port=port, certificate=cert)

    token = d._get_session_token()
    print(token)

    # 启动应用,并且获取pid
    pid = d.frida.spawn("sa.friendimobile.vm")
    d.frida.resume(pid)


    # time.sleep(0.5)
    session = d.frida.attach(pid)
    session.on("detached", print)

    path = os.path.dirname(os.path.realpath(__file__))
    local_path = path.split("xiaosuan_box")[0] + "xiaosuan_box\hook\hook.js"

    hook_js = open(local_path,encoding='utf-8').read()

    sc = session.create_script(hook_js)

    sc.on("destroyed", print)
    sc.on("message", print)
    sc.load()
    sc.eternalize()
    exit (0)


run_frida()
