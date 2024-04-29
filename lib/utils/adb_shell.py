import logging, os
from subprocess import Popen, PIPE

# 初始化日志记录器
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("ADBShell")


def exec_command(cmd: str, quiet=False, suppress_error=False):
    result = {'out': [], 'err': []}
    if not quiet:
        log.debug(f"Executing command: {cmd}")

    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, close_fds=True)
    out, err = process.communicate()

    if out:
        result['out'] = out.decode('utf-8', errors='replace').strip().split('\n')
        if not quiet:
            log.debug(f"Output: {out.decode('utf-8', errors='replace').strip()}")
    else:
        result['out'] = ["No output returned."]

    if err:
        result['err'] = err.decode('utf-8', errors='replace').strip().split('\n')
        if not suppress_error:
            log.error(f"Error: {err.decode('utf-8', errors='replace').strip()}")
        else:
            log.debug(f"Suppressed Error: {err.decode('utf-8', errors='replace').strip()}")
    else:
        result['err'] = ["No errors."]

    return result


def start_scrcpy(serial):

    """
    启动 scrcpy 以显示和控制连接的 Android 设备。
    """

    cmd = ['./scrcpy/scrcpy.exe', '-s', serial]
    print("当前工作目录:", os.getcwd())
    log.debug("Starting scrcpy with command: " + ' '.join(cmd))
    return exec_command(' '.join(cmd))


def adb_devices():
    """
    获取当前通过 ADB 连接的设备列表。
    """
    return exec_command('adb devices', quiet=True)


def adb_push(serial, src, dst):
    """
    将文件从本地推送到设备指定路径。
    """
    cmd = f'adb -s {serial} push "{src}" "{dst}"'
    return exec_command(cmd)


def adb_reverse(serial, port):
    """
    设置设备端口到本地端口的反向映射。
    """
    cmd = f'adb -s {serial} reverse tcp:{port} tcp:{port}'
    return exec_command(cmd)


def adb_forward(serial, local_port, remote_port):
    """
    设置本地端口到设备端口的正向映射。
    """
    cmd = f'adb -s {serial} forward tcp:{local_port} tcp:{remote_port}'
    return exec_command(cmd)


def adb_clear_forward(serial, local_port):
    """
    清除设置的正向端口映射。
    """
    cmd = f'adb -s {serial} forward --remove tcp:{local_port}'
    return exec_command(cmd)


"""
在设备上执行任意 ADB 命令。
"""
def adb_execute_command(serial, command):
    cmd = f'adb -s {serial} {command}'
    return exec_command(cmd)

