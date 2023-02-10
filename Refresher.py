import schedule
import time
import subprocess
from gc import collect, enable
def run_program():
    subprocess.call(["python", "main.py"])

schedule.every(1).minutes.do(run_program)

while True:
    schedule.run_pending()
    time.sleep(1)
enable()
collect()