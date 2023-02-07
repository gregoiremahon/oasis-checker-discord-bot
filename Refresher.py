import schedule
import time
import subprocess

def run_program():
    subprocess.call(["python3", "oasis-checker-discord-bot/main.py"])

schedule.every(1).minutes.do(run_program)

while True:
    schedule.run_pending()
    time.sleep(1)