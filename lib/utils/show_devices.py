from lib.utils import adb_shell

def get_device_info(device_id):
    a = {}
    a['设备ID'] = f'{device_id}'

    # 检查设备是否处于系统模式
    try:
        state_output = adb_shell.exec_command(f'adb -s {device_id} get-state',True)
        if "device" in state_output['out']:
            a['设备状态'] = '系统模式'
    except:
        pass

    # 检查设备是否处于fastboot模式
    try:
        fastboot_devices = adb_shell.exec_command(f'fastboot devices',True)
        if device_id in fastboot_devices['out']:
            a['设备状态'] = 'Fastboot模式'
    except:
        pass

    # 检查设备是否处于recovery模式
    try:
        # ADB命令行不能直接检测Recovery模式，此处假定设备不在线且不在Fastboot则可能在Recovery
        # 通常需要特定命令或日志检测确认
        adb_devices = adb_shell.exec_command(f'adb -s {device_id} devices',True)
        if "recovery" in adb_devices['out']:
            a['设备状态'] = 'Recovery模式'
        else:

            a['设备状态'] = '设备可能处于Recovery模式或已断开连接'

    except:
        a['设备状态'] = '无法确定设备状态'

    # 获取VAB状态
    try:
        slots_output = adb_shell.exec_command(f'adb -s {device_id} shell getprop ro.boot.slot_suffix',True)
        slot_suffix = slots_output['out'][0]
        if slot_suffix:
            a['VAB状态'] = f'槽位{slot_suffix.upper()}'
        else:
            a['VAB状态'] = f'设备可能不支持A/B槽位。'
    except:
        a['VAB状态'] = f'无法获取VAB状态。'

    # 获取设备代码
    try:
        product_output = adb_shell.exec_command(f"adb -s {device_id} shell getprop ro.product.name",True)
        product_name = product_output['out'][0]
        a['设备名称'] = f'{product_name}'
    except:
        a['设备名称'] = f'无法获取设备代码。'

    # 检查是否Root (还未完善)
    try:
        root_output = adb_shell.exec_command(f"adb -s {device_id} shell getprop ro.root_device",True)
        if "root" in root_output['out']:
            a['Root状态'] = f'已Root'
        else:
            a['Root状态'] = f'未Root'
    except:
        a['Root状态'] = f'无法检查Root状态。'
    return a

def show_devices():
    """
    获取并显示所有通过 ADB 连接的设备的序列号。
    """
    devices_list = []
    result = adb_shell.adb_devices()
    if result['out']:
        for line in result['out']:
            if "\tdevice" in line:
                # 设备序列号通常在输出的行中，通过制表符\t分隔
                device_id = line.split("\t")[0]
                devices_list.append(device_id)

    return devices_list



def button_back(device_id):
    adb_shell.exec_command('adb -s {} shell input keyevent KEYCODE_BACK'.format(device_id),True)
def button_home(device_id):
    adb_shell.exec_command('adb -s {} shell input keyevent KEYCODE_HOME'.format(device_id),True)
def button_recent(device_id):
    adb_shell.exec_command('adb -s {} shell input keyevent KEYCODE_APP_SWITCH'.format(device_id),True)

