#!/bin/bash

# 打开设置应用
am start -a android.settings.SETTINGS

# 等待3秒
sleep 3

# 关闭设置应用
am force-stop com.android.settings
