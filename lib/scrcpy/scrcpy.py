import subprocess,os
from lib.utils import adb_shell
def start_scrcpy(serial, options="--no-audio"):
    path = os.path.dirname(os.path.realpath(__file__))
    command = f"{path}\scrcpy.exe -s {serial} {options}"
    try:
        # 使用subprocess.run启动scrcpy，capture_output=True来捕获输出
        # subprocess.run(command, capture_output=True, text=True, check=True)
        adb_shell.exec_command(command,True)
    except:
        print("Failed to start scrcpy.")



# start_scrcpy("8KB0223225000457")