import subprocess,os

def start_scrcpy(serial, options="--no-audio"):
    path = os.path.dirname(os.path.realpath(__file__))
    command = f"{path}\scrcpy.exe -s {serial} {options}"
    try:
        # 使用subprocess.run启动scrcpy，capture_output=True来捕获输出
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("Scrcpy started successfully.")
        print("Output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to start scrcpy.")
        print("Error:", e.stderr)
