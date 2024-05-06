import os
from os.path import isfile
from lamda.client import *


def pubkey(device,action):
    certfile = os.environ.get("CERTIFICATE", None)
    port = int(os.environ.get("PORT", 65000))
    android_path = os.path.join("~", ".android")
    abs_android_path = os.path.expanduser(android_path)
    f = "adbkey.pub"  # 默认的公钥文件名
    d = Device(device, port=port, certificate=certfile)

    if action == 'install':
        cmd = 'install'
        os.chdir(abs_android_path)

        # 尝试生成公钥文件
        pubkey = os.popen("adb pubkey adbkey").read()
        open("adbkey.lamda", "w").write(pubkey)

        f = ("adbkey.lamda", f)[isfile(f)]

        call = getattr(d, "%s_adb_pubkey" % cmd)
        exit(not call(f))

    elif action == 'uninstall':
        cmd = 'uninstall'
        os.chdir(abs_android_path)
        pubkey = os.popen("adb pubkey adbkey").read()
        open("adbkey.lamda", "w").write(pubkey)
        f = ("adbkey.lamda", f)[isfile(f)]

        call = getattr(d, "%s_adb_pubkey" % cmd)
        exit(not call(f))