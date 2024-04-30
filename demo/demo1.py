from lib.utils import adb_shell





file = adb_shell.exec_command('adb -s LNG0123525000370 ls -l /',True)['out']

for i in file:
    print(i.split('\r')[0].split(' ')[-1])