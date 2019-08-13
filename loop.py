import subprocess

while True:
    try:
        print (subprocess.check_output(['python', 'main.py']))
    except KeyboardInterrupt:
        break